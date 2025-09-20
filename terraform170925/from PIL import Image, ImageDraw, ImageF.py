from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

def create_milk_statement(p_number, from_date, to_date, payment, incentive, deductions, net_payment, save_path):
    # Create a blank white image
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)

    # Fonts (default)
    title_font = ImageFont.truetype("arial.ttf", 40)
    label_font = ImageFont.truetype("arial.ttf", 30)
    small_font = ImageFont.truetype("arial.ttf", 26)

    # Draw header (P-1, etc.)
    draw.text((20, 20), f"P-{p_number}", fill="black", font=title_font)

    # Draw 'From' and 'To' dates
    draw.text((20, 100), f"From Date: {from_date}", fill="black", font=label_font)
    draw.text((20, 150), f"To Date:   {to_date}", fill="black", font=label_font)

    # Draw payment info
    y = 230
    spacing = 50
    draw.text((20, y), f"Payment: ₹{payment:,.2f}", fill="black", font=label_font)
    draw.text((20, y + spacing), f"Incentive: ₹{incentive:,.2f}", fill="black", font=label_font)
    draw.text((20, y + 2 * spacing), f"Deductions: ₹{deductions:,.2f}", fill="black", font=label_font)

    # Draw net payment
    draw.text((20, y + 3.5 * spacing), f"Net Payment: ₹{net_payment:,.2f}", fill="green", font=label_font)

    # Fake download and view icons (placeholders)
    draw.rectangle((700, 30, 740, 70), fill="gray")  # Download
    draw.rectangle((750, 30, 790, 70), fill="gray")  # Eye

    draw.text((705, 35), "↓", fill="white", font=label_font)
    draw.text((755, 35), "👁", fill="white", font=label_font)

    # Save image
    img.save(save_path)
    print(f"Saved: {save_path}")


# Example usage:
create_milk_statement(
    p_number=1,
    from_date="01-Sep-2024",
    to_date="10-Sep-2024",
    payment=122000.00,
    incentive=20400.00,
    deductions=0.00,
    net_payment=142400.00,
    save_path="P1_Sep2024.png"
)
