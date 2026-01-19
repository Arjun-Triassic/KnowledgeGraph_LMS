"""
Email service for sending notifications via aiosmtplib.
Supports HTML templates and async email sending.
"""
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

import aiosmtplib
from jinja2 import Template

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class EmailService:
    """Service for sending emails asynchronously."""

    def __init__(self):
        self.smtp_host = settings.smtp_host
        self.smtp_port = settings.smtp_port
        self.smtp_user = settings.smtp_user
        self.smtp_password = settings.smtp_password
        self.smtp_from = settings.smtp_from_email or settings.smtp_user
        self.use_tls = settings.smtp_use_tls

    async def send_email_async(
        self,
        to_email: str,
        subject: str,
        html_body: str,
        text_body: Optional[str] = None,
    ) -> bool:
        """
        Send an email asynchronously.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_body: HTML email body
            text_body: Optional plain text body (defaults to stripped HTML)
            
        Returns:
            True if email was sent successfully, False otherwise
        """
        if not self.smtp_host or not self.smtp_user or not self.smtp_password:
            logger.warning("Email configuration not set. Skipping email send.")
            return False

        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["From"] = self.smtp_from
            message["To"] = to_email
            message["Subject"] = subject

            # Add text and HTML parts
            if text_body:
                message.attach(MIMEText(text_body, "plain"))
            else:
                # Simple HTML stripping for text fallback
                import re
                text_body = re.sub(r"<[^>]+>", "", html_body)
                message.attach(MIMEText(text_body, "plain"))

            message.attach(MIMEText(html_body, "html"))

            # Send email
            await aiosmtplib.send(
                message,
                hostname=self.smtp_host,
                port=self.smtp_port,
                username=self.smtp_user,
                password=self.smtp_password,
                use_tls=self.use_tls,
            )

            logger.info(f"Email sent successfully to {to_email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}", exc_info=True)
            return False

    async def send_email_from_template(
        self,
        to_email: str,
        subject: str,
        template_string: str,
        template_vars: dict,
        text_template_string: Optional[str] = None,
    ) -> bool:
        """
        Send an email using a Jinja2 template.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            template_string: Jinja2 HTML template string
            template_vars: Variables to render in template
            text_template_string: Optional plain text template
            
        Returns:
            True if email was sent successfully, False otherwise
        """
        # Render HTML template
        html_template = Template(template_string)
        html_body = html_template.render(**template_vars)

        # Render text template if provided
        text_body = None
        if text_template_string:
            text_template = Template(text_template_string)
            text_body = text_template.render(**template_vars)

        return await self.send_email_async(to_email, subject, html_body, text_body)


# Email templates
ENROLLMENT_NOTIFICATION_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background-color: #4CAF50; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background-color: #f9f9f9; }
        .button { display: inline-block; padding: 10px 20px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Welcome to {{ course_title }}!</h1>
        </div>
        <div class="content">
            <p>Hello {{ user_name }},</p>
            <p>You have been successfully enrolled in the course <strong>{{ course_title }}</strong>.</p>
            <p>We're excited to have you on this learning journey!</p>
            <p>
                <a href="#" class="button">Start Learning</a>
            </p>
            <p>Best regards,<br>The KnowledgeGraph LMS Team</p>
        </div>
    </div>
</body>
</html>
"""

SUBMISSION_NOTIFICATION_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background-color: #2196F3; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background-color: #f9f9f9; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>New Submission Received</h1>
        </div>
        <div class="content">
            <p>Hello {{ instructor_name }},</p>
            <p>A new submission has been received for <strong>{{ assessment_title }}</strong>.</p>
            <p><strong>Student:</strong> {{ student_name }}</p>
            <p><strong>Submitted:</strong> {{ submission_date }}</p>
            <p>Please review the submission at your earliest convenience.</p>
            <p>Best regards,<br>The KnowledgeGraph LMS Team</p>
        </div>
    </div>
</body>
</html>
"""

COURSE_COMPLETION_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background-color: #FF9800; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background-color: #f9f9f9; }
        .button { display: inline-block; padding: 10px 20px; background-color: #FF9800; color: white; text-decoration: none; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎉 Course Completed!</h1>
        </div>
        <div class="content">
            <p>Hello {{ user_name }},</p>
            <p>Congratulations! You have successfully completed the course <strong>{{ course_title }}</strong>.</p>
            <p>Your certificate is ready for download.</p>
            <p>
                <a href="#" class="button">Download Certificate</a>
            </p>
            <p>Keep up the great work!</p>
            <p>Best regards,<br>The KnowledgeGraph LMS Team</p>
        </div>
    </div>
</body>
</html>
"""

PROGRESS_REPORT_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background-color: #9C27B0; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background-color: #f9f9f9; }
        .progress-bar { background-color: #e0e0e0; border-radius: 10px; padding: 3px; margin: 10px 0; }
        .progress-fill { background-color: #9C27B0; height: 20px; border-radius: 7px; text-align: center; color: white; line-height: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Weekly Progress Report</h1>
        </div>
        <div class="content">
            <p>Hello {{ user_name }},</p>
            <p>Here's your weekly progress summary:</p>
            {% for course in courses %}
            <div style="margin: 20px 0; padding: 15px; background-color: white; border-radius: 5px;">
                <h3>{{ course.title }}</h3>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {{ course.progress }}%;">
                        {{ course.progress }}%
                    </div>
                </div>
            </div>
            {% endfor %}
            <p>Keep up the great work!</p>
            <p>Best regards,<br>The KnowledgeGraph LMS Team</p>
        </div>
    </div>
</body>
</html>
"""
