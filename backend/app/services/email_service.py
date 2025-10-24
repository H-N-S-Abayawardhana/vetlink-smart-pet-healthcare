import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

async def send_appointment_notification_to_vet(data: Dict[str, Any]) -> Dict[str, Any]:
    """Send email notification to veterinarian when user schedules an appointment."""
    try:
        # Check if email configuration is available
        if not all([settings.SMTP_HOST, settings.SMTP_USER, settings.SMTP_PASS, settings.SMTP_FROM_EMAIL]):
            logger.warning("Email configuration incomplete, skipping email notification")
            return {"success": False, "error": "Email configuration incomplete"}
        
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = f"New Appointment Request - {data['appointment_date']} at {data['appointment_time']}"
        message["From"] = f"VetLink <{settings.SMTP_FROM_EMAIL}>"
        message["To"] = data["veterinarian_email"]
        
        # Create HTML content
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
          <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px;">
            <h2 style="color: #2c3e50; margin-bottom: 20px;">New Appointment Request</h2>
            
            <div style="background-color: white; padding: 20px; border-radius: 6px; margin-bottom: 20px;">
              <h3 style="color: #34495e; margin-bottom: 15px;">Appointment Details</h3>
              <table style="width: 100%; border-collapse: collapse;">
                <tr>
                  <td style="padding: 8px 0; font-weight: bold; color: #555;">Appointment ID:</td>
                  <td style="padding: 8px 0; color: #333;">#{data['appointment_id']}</td>
                </tr>
                <tr>
                  <td style="padding: 8px 0; font-weight: bold; color: #555;">Date:</td>
                  <td style="padding: 8px 0; color: #333;">{data['appointment_date']}</td>
                </tr>
                <tr>
                  <td style="padding: 8px 0; font-weight: bold; color: #555;">Time:</td>
                  <td style="padding: 8px 0; color: #333;">{data['appointment_time']}</td>
                </tr>
                {f'<tr><td style="padding: 8px 0; font-weight: bold; color: #555;">Reason:</td><td style="padding: 8px 0; color: #333;">{data["reason"]}</td></tr>' if data.get("reason") else ""}
              </table>
            </div>

            <div style="background-color: white; padding: 20px; border-radius: 6px; margin-bottom: 20px;">
              <h3 style="color: #34495e; margin-bottom: 15px;">Client Information</h3>
              <table style="width: 100%; border-collapse: collapse;">
                <tr>
                  <td style="padding: 8px 0; font-weight: bold; color: #555;">Name:</td>
                  <td style="padding: 8px 0; color: #333;">{data['user_name']}</td>
                </tr>
                <tr>
                  <td style="padding: 8px 0; font-weight: bold; color: #555;">Email:</td>
                  <td style="padding: 8px 0; color: #333;">{data['user_email']}</td>
                </tr>
                <tr>
                  <td style="padding: 8px 0; font-weight: bold; color: #555;">Contact:</td>
                  <td style="padding: 8px 0; color: #333;">{data['user_contact']}</td>
                </tr>
              </table>
            </div>

            <div style="background-color: #e8f5e8; padding: 15px; border-radius: 6px; border-left: 4px solid #28a745;">
              <p style="margin: 0; color: #155724; font-weight: bold;">
                Please log in to your VetLink dashboard to confirm or reject this appointment.
              </p>
            </div>
          </div>
        </div>
        """
        
        # Attach HTML content
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)
        
        # Send email
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            use_tls=not settings.SMTP_SECURE,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASS,
        )
        
        logger.info(f"Appointment notification sent to veterinarian: {data['veterinarian_email']}")
        return {"success": True, "message": "Email sent successfully"}
        
    except Exception as error:
        logger.error(f"Error sending appointment notification to veterinarian: {error}")
        return {"success": False, "error": str(error)}

async def send_appointment_status_to_user(data: Dict[str, Any]) -> Dict[str, Any]:
    """Send email to user when veterinarian confirms or rejects appointment."""
    try:
        # Check if email configuration is available
        if not all([settings.SMTP_HOST, settings.SMTP_USER, settings.SMTP_PASS, settings.SMTP_FROM_EMAIL]):
            logger.warning("Email configuration incomplete, skipping email notification")
            return {"success": False, "error": "Email configuration incomplete"}
        
        is_accepted = data["status"] == "accepted"
        status_color = "#28a745" if is_accepted else "#dc3545"
        status_text = "Confirmed" if is_accepted else "Rejected"
        status_icon = "✅" if is_accepted else "❌"
        
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Appointment {status_text} - {data['appointment_date']} at {data['appointment_time']}"
        message["From"] = f"VetLink <{settings.SMTP_FROM_EMAIL}>"
        message["To"] = data["user_email"]
        
        # Create HTML content
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
          <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px;">
            <h2 style="color: #2c3e50; margin-bottom: 20px;">
              {status_icon} Appointment {status_text}
            </h2>
            
            <div style="background-color: white; padding: 20px; border-radius: 6px; margin-bottom: 20px;">
              <h3 style="color: #34495e; margin-bottom: 15px;">Appointment Details</h3>
              <table style="width: 100%; border-collapse: collapse;">
                <tr>
                  <td style="padding: 8px 0; font-weight: bold; color: #555;">Appointment ID:</td>
                  <td style="padding: 8px 0; color: #333;">#{data['appointment_id']}</td>
                </tr>
                <tr>
                  <td style="padding: 8px 0; font-weight: bold; color: #555;">Date:</td>
                  <td style="padding: 8px 0; color: #333;">{data['appointment_date']}</td>
                </tr>
                <tr>
                  <td style="padding: 8px 0; font-weight: bold; color: #555;">Time:</td>
                  <td style="padding: 8px 0; color: #333;">{data['appointment_time']}</td>
                </tr>
                <tr>
                  <td style="padding: 8px 0; font-weight: bold; color: #555;">Status:</td>
                  <td style="padding: 8px 0; color: {status_color}; font-weight: bold;">{status_text}</td>
                </tr>
                {f'<tr><td style="padding: 8px 0; font-weight: bold; color: #555;">Reason:</td><td style="padding: 8px 0; color: #333;">{data["reason"]}</td></tr>' if data.get("reason") else ""}
              </table>
            </div>

            <div style="background-color: white; padding: 20px; border-radius: 6px; margin-bottom: 20px;">
              <h3 style="color: #34495e; margin-bottom: 15px;">Veterinarian Information</h3>
              <table style="width: 100%; border-collapse: collapse;">
                <tr>
                  <td style="padding: 8px 0; font-weight: bold; color: #555;">Name:</td>
                  <td style="padding: 8px 0; color: #333;">{data['veterinarian_name']}</td>
                </tr>
                <tr>
                  <td style="padding: 8px 0; font-weight: bold; color: #555;">Email:</td>
                  <td style="padding: 8px 0; color: #333;">{data['veterinarian_email']}</td>
                </tr>
                <tr>
                  <td style="padding: 8px 0; font-weight: bold; color: #555;">Contact:</td>
                  <td style="padding: 8px 0; color: #333;">{data['veterinarian_contact']}</td>
                </tr>
              </table>
            </div>

            {f'''
            <div style="background-color: #e8f5e8; padding: 15px; border-radius: 6px; border-left: 4px solid #28a745;">
              <p style="margin: 0; color: #155724; font-weight: bold;">
                Great! Your appointment has been confirmed. Please arrive 10 minutes early for your appointment.
              </p>
            </div>
            ''' if is_accepted else f'''
            <div style="background-color: #f8d7da; padding: 15px; border-radius: 6px; border-left: 4px solid #dc3545;">
              <p style="margin: 0; color: #721c24; font-weight: bold;">
                Unfortunately, your appointment request has been rejected. Please contact the veterinarian or schedule a different time slot.
              </p>
            </div>
            '''}
          </div>
        </div>
        """
        
        # Attach HTML content
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)
        
        # Send email
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            use_tls=not settings.SMTP_SECURE,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASS,
        )
        
        logger.info(f"Appointment status notification sent to user: {data['user_email']}")
        return {"success": True, "message": "Email sent successfully"}
        
    except Exception as error:
        logger.error(f"Error sending appointment status notification to user: {error}")
        return {"success": False, "error": str(error)}
