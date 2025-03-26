import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from aiosmtplib import SMTP
from fastapi import HTTPException
from jinja2 import Environment, FileSystemLoader, select_autoescape

from loan_advisory_service.main.config import EmailConfig


class EmailService:
    def __init__(self, config: EmailConfig) -> None:
        self.config = config

        self.jinja_env = Environment(
            loader=FileSystemLoader(config.templates_dir),
            enable_async=True,
            autoescape=select_autoescape(["html"]),
        )

    async def _render_template(
            self, context: dict[str, str | int], template_name: str
    ) -> tuple[str, str]:
        html_template = self.jinja_env.get_template(f"{template_name}.html")
        html_content = await html_template.render_async(**context)

        text_template = self.jinja_env.get_template(f"{template_name}.txt")
        text_content = await text_template.render_async(**context)

        return html_content, text_content

    async def send_verification_email(
            self, to_email: str, link: str, expires_in: int
    ) -> None:
        html_content, text_content = await self._render_template(
            context={"link": link, "expires_in": expires_in},
            template_name="verification",
        )

        return await self._send_email(
            to_email=to_email,
            html=html_content,
            text=text_content,
            subject="Email Confirmation",
        )

    async def send_password_reset_email(
            self, to_email: str, link: str, expires_in: int
    ) -> None:
        html_content, text_content = await self._render_template(
            context={"link": link, "expires_in": expires_in},
            template_name="reset_password",
        )

        return await self._send_email(
            to_email=to_email,
            html=html_content,
            text=text_content,
            subject="Password reset",
        )

    async def send_email_changing_link(
            self, to_email: str, link: str, expires_in: int
    ) -> None:
        html_content, text_content = await self._render_template(
            context={"link": link, "expires_in": expires_in},
            template_name="change_email",
        )
        return await self._send_email(
            to_email=to_email,
            html=html_content,
            text=text_content,
            subject="Confirm email changing",
        )

    async def send_apply_link(self, to_email: str, link: str):
        html_content, text_content = await self._render_template(
            context={"link": link},
            template_name="invite_to_apply",
        )
        return await self._send_email(
            to_email=to_email,
            html=html_content,
            text=text_content,
            subject="Invite to request",
        )

    async def _send_email(self, to_email, html: str, text: str, subject: str) -> None:
        message = MIMEMultipart("alternative")
        message["From"] = self.config.username
        message["To"] = to_email
        message["Subject"] = subject

        message.attach(MIMEText(text, "plain"))
        message.attach(MIMEText(html, "html"))

        try:
            async with SMTP(
                    hostname=self.config.host,
                    port=self.config.port,
                    username=self.config.username,
                    password=self.config.password,
                    start_tls=True,
            ) as client:
                await client.send_message(message)
        except Exception as e:
            logging.error(f"Error while sending email: {e}")
            raise HTTPException(
                status_code=500,
                detail="Error while sending email. Please, try again later",
            )
