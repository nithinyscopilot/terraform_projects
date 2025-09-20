from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta
import calendar
import random
from fpdf import FPDF
import os

def generate_realistic_numbers():
    # Base milk payment (adjusted to keep final amount under 1.2 lakhs)
    # Calculate backwards from target net payment
    target_net = random.uniform(100000, 120000)  # Target final amount under 1.2 lakhs
    
    # Calculate deductions (feed costs)
    deductions = random.uniform(12000, 18500)  # Approximately 10-15 bags worth
    
    # Calculate base payment needed to reach target after incentive and deductions
    # Assuming 10% average incentive, solve for base payment:
    # base + (base * 0.1) - deductions = target_net
    # base * 1.1 = target_net + deductions
    target_base = (target_net + deductions) / 1.1
    
    # Now adjust liters and rate to match this base payment
    rate_per_liter = random.uniform(50, 60)
    liters_per_day = target_base / (rate_per_liter * 10)  # 10 days period
    
    payment = target_base
    incentive = payment * random.uniform(0.05, 0.15)  # Still keep 5-15% incentive
    
    net_payment = payment + incentive - deductions
    
    # We're not showing deductions detail anymore
    deductions_detail = ""
    
    return payment, incentive, deductions, net_payment, deductions_detail

def create_milk_statement(p_number, from_date, to_date, payment, incentive, deductions, net_payment, save_path, deductions_detail):
    # Create a blank white image with light blue background
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)

    # Fonts (default)
    title_font = ImageFont.truetype("arial.ttf", 40)
    header_font = ImageFont.truetype("arial.ttf", 36)
    label_font = ImageFont.truetype("arial.ttf", 28)
    value_font = ImageFont.truetype("arial.ttf", 28)
    
    # Colors
    header_color = (25, 25, 112)  # Dark blue
    label_color = (70, 70, 70)    # Dark gray
    value_color = (0, 0, 0)       # Black
    net_color = (34, 139, 34)     # Forest green
    
    # Draw header background
    draw.rectangle([0, 0, 800, 70], fill=(240, 248, 255))  # Light blue header
    draw.line([0, 70, 800, 70], fill=(200, 200, 200), width=2)
    
    # Draw title
    draw.text((30, 15), "PAYMENT STATEMENT", fill=header_color, font=title_font)
    draw.text((650, 20), f"P-{p_number}", fill=header_color, font=header_font)
    
    # Draw period box
    period_y = 90
    draw.rectangle([30, period_y, 770, period_y + 80], outline=(200, 200, 200), width=1)
    draw.text((50, period_y + 10), f"Period: {from_date} to {to_date}", fill=label_color, font=label_font)
    
    # Draw payment info with proper alignment
    content_y = 200
    spacing = 60
    col1_x = 50   # Labels
    col2_x = 300  # Values
    
    # Helper function for drawing rows
    def draw_row(y, label, value, label_color=label_color, value_color=value_color):
        draw.text((col1_x, y), label, fill=label_color, font=label_font)
        draw.text((col2_x, y), f"₹ {value:,.2f}", fill=value_color, font=value_font)
    
    # Draw payment details
    draw_row(content_y, "Base Payment:", payment)
    draw_row(content_y + spacing, "Incentive:", incentive)
    draw_row(content_y + 2 * spacing, "Deductions:", deductions)
    
    # Draw separator line before net payment
    line_y = content_y + 3 * spacing - 10
    draw.line([col1_x, line_y, 750, line_y], fill=(200, 200, 200), width=2)
    
    # Draw net payment with bold appearance
    draw_row(content_y + 3 * spacing, "Net Payment:", net_payment, net_color, net_color)
    
    # Save image with high quality
    img.save(save_path, quality=95)

    # Fake download and view icons (placeholders)
    draw.rectangle((700, 30, 740, 70), fill="gray")  # Download
    draw.rectangle((750, 30, 790, 70), fill="gray")  # Eye

    draw.text((705, 35), "↓", fill="white", font=label_font)
    draw.text((755, 35), "👁", fill="white", font=label_font)

    # Save image
    img.save(save_path)
    print(f"Generated statement for {from_date} to {to_date}")
    return save_path

def create_yearly_statements():
    # Create output directory if it doesn't exist
    if not os.path.exists('statements'):
        os.makedirs('statements')

    image_files = []
    start_date = datetime(2024, 9, 1)
    
    # Generate statements for each month from September 2024 to August 2025
    for i in range(12):  # 12 months
        current_date = start_date + timedelta(days=30*i)
        
        # Skip if we're past August 2025
        if current_date.year > 2025 or (current_date.year == 2025 and current_date.month > 8):
            continue
            
        # Calculate the last day of the month
        _, last_day = calendar.monthrange(current_date.year, current_date.month)
        
        # Generate one statement per 10-day period (P1 for 1-10, P2 for 11-20, P3 for 21-end)
        periods = [
            (1, "01", "10"),      # P1 for first 10 days
            (2, "11", "20"),      # P2 for days 11-20
            (3, "21", str(last_day))  # P3 for remaining days
        ]
        
        for p_number, start_day, end_day in periods:
            payment, incentive, deductions, net_payment, _ = generate_realistic_numbers()
            save_path = f"statements/P{p_number}_{current_date.strftime('%b%Y')}.png"
            image_files.append(create_milk_statement(
                p_number=p_number,
                from_date=f"{start_day}-{current_date.strftime('%b-%Y')}",
                to_date=f"{end_day}-{current_date.strftime('%b-%Y')}",
                payment=payment,
                incentive=incentive,
                deductions=deductions,
                net_payment=net_payment,
                save_path=save_path,
                deductions_detail=""
            ))

    # Create PDF from all statements
    pdf = FPDF()
    for image_file in image_files:
        pdf.add_page()
        pdf.image(image_file, x=10, y=10, w=190)
    
    pdf_path = "statements/yearly_statements.pdf"
    pdf.output(pdf_path)
    print(f"\nCreated combined PDF: {pdf_path}")
    
    # Copy to Downloads folder
    import shutil
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    shutil.copy2(pdf_path, os.path.join(downloads_path, "yearly_statements.pdf"))
    print(f"PDF copied to Downloads folder")

if __name__ == "__main__":
    create_yearly_statements()