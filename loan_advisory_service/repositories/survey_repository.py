from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from loan_advisory_service.db.models.admin.answer_option import AnswerOption
from loan_advisory_service.db.models.admin.question import Question
from loan_advisory_service.db.models.admin.question_group import QuestionGroup
from loan_advisory_service.schemas.survey import QuestionGroupSchemaCreate, QuestionGroupUpdateSchema, \
    AnswerOptionUpdateSchema, QuestionGroupSchemaResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException


class SurveyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_question_group(self, data: QuestionGroupSchemaCreate) -> QuestionGroupSchemaResponse:
        try:
            group = QuestionGroup(title=data.title, order=data.order)
            self.session.add(group)
            await self.session.flush()

            for q in data.questions:
                question = Question(
                    text=q.text,
                    type=q.type.value,
                    order=q.order,
                    group_id=group.id
                )
                self.session.add(question)
                await self.session.flush()

                if q.options:
                    for opt in q.options:
                        option = AnswerOption(text=opt.text, question_id=question.id)
                        self.session.add(option)

            await self.session.commit()
            await self.session.refresh(group)

            query = (
                select(QuestionGroup)
                .options(joinedload(QuestionGroup.questions).joinedload(Question.options))
                .filter(QuestionGroup.id == group.id)
            )
            result = await self.session.execute(query)
            group = result.unique().scalar_one()

            return QuestionGroupSchemaResponse.model_validate(group)

        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(status_code=400, detail="A question group with this order already exists.")
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    # async def update_group(self, group_id: int, data: QuestionGroupUpdateSchema) -> QuestionGroupSchemaResponse:
    #     query = (
    #         select(QuestionGroup)
    #         .options(joinedload(QuestionGroup.questions).joinedload(Question.options))
    #         .filter(QuestionGroup.id == group_id)
    #         .limit(1)
    #     )
    #     result = await self.session.execute(query)
    #     group = result.scalars().first()
    #     if not group:
    #         raise HTTPException(status_code=404, detail=f"Question Group with ID {group_id} not found")
    #
    #     if data.title is not None:
    #         group.title = data.title
    #     if data.order is not None:
    #         group.order = data.order
    #
    #     if data.questions is not None:
    #         existing_questions = {q.id: q for q in group.questions}
    #         question_ids_in_request = {q_data.id for q_data in data.questions if q_data.id}
    #
    #         for q_data in data.questions:
    #             if q_data.id:
    #                 question = existing_questions.get(q_data.id)
    #                 if question:
    #                     if q_data.text is not None:
    #                         question.text = q_data.text
    #                     if q_data.type is not None:
    #                         question.type = q_data.type
    #                     if q_data.order is not None:
    #                         question.order = q_data.order
    #
    #                     await self._update_options(question, q_data.options)
    #
    #             else:
    #                 new_question = Question(
    #                     text=q_data.text,
    #                     type=q_data.type,
    #                     order=q_data.order,
    #                     group_id=group.id,
    #                 )
    #                 self.session.add(new_question)
    #                 question_ids_in_request.add(new_question.id)
    #                 await self.session.flush()
    #                 if q_data.options:
    #                     for opt_data in q_data.options:
    #                         self.session.add(AnswerOption(text=opt_data.text, question_id=new_question.id))
    #         for question in group.questions:
    #             if question.id not in question_ids_in_request:
    #                 await self.session.delete(question)
    #
    #         # try:
    #         await self.session.commit()
    #     # except IntegrityError:
    #     #     await self.session.rollback()
    #     #     raise HTTPException(status_code=400, detail="A question group with this order already exists.")
    #     # except SQLAlchemyError as e:
    #     #     await self.session.rollback()
    #     #     raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    #     # except Exception as e:
    #     #     await self.session.rollback()
    #     #     raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    #
    #     return QuestionGroupSchemaResponse.model_validate(group, )
    #
    # async def _update_options(self, question: Question, options_data: list[AnswerOptionUpdateSchema]) -> None:
    #     if options_data is None:
    #         return
    #
    #     existing_options = {opt.id: opt for opt in question.options}
    #     option_ids_in_request = {opt_data.id for opt_data in options_data if opt_data.id}
    #
    #     for opt_data in options_data:
    #         if opt_data.id:
    #             option = existing_options.get(opt_data.id)
    #             if option:
    #                 option.text = opt_data.text
    #         else:
    #             new_option = AnswerOption(text=opt_data.text, question_id=question.id)
    #             self.session.add(new_option)
    #
    #     for option in question.options:
    #         if option.id not in option_ids_in_request:
    #             await self.session.delete(option)
