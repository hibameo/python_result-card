import streamlit as st
from fpdf import FPDF

# Function to calculate grade
def calculate_grade(marks, total_marks):
    percentage = (marks / total_marks) * 100
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "F"

# Function to generate PDF
def generate_pdf(student_name, father_name, roll_no, student_class, subjects):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", "B", 14)
    pdf.cell(190, 10, "AL-HAMD CADET SCHOOLING SYSTEM", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(190, 10, "KARACHI", ln=True, align="C")
    pdf.cell(190, 10, "STATEMENT OF MARKS", ln=True, align="C")
    pdf.cell(190, 10, "FINAL TERM EXAMINATION", ln=True, align="C")
    pdf.ln(10)

    # Student Info
    pdf.set_font("Arial", "", 12)
    pdf.cell(50, 8, f"Name: {student_name}", ln=True)
    pdf.cell(50, 8, f"Father Name: {father_name}", ln=True)
    pdf.cell(50, 8, f"Class: {student_class}", ln=True)
    pdf.cell(50, 8, f"Roll No: {roll_no}", ln=True)
    pdf.ln(5)

    # Table Header
    pdf.set_font("Arial", "B", 10)
    pdf.cell(60, 8, "Subjects", 1)
    pdf.cell(40, 8, "Total Marks", 1)
    pdf.cell(40, 8, "Marks Obtained", 1)
    pdf.cell(25, 8, "Grade", 1)
    pdf.cell(25, 8, "Remarks", 1)
    pdf.ln()

    # Table Content
    total_obtained = 0
    total_marks = 0
    pdf.set_font("Arial", "", 10)
    for sub in subjects:
        grade = calculate_grade(sub["marks"], sub["total_marks"])
        pdf.cell(60, 8, sub["name"], 1)
        pdf.cell(40, 8, str(sub["total_marks"]), 1)
        pdf.cell(40, 8, str(sub["marks"]), 1)
        pdf.cell(25, 8, grade, 1)
        pdf.cell(25, 8, "PASS" if grade != "F" else "FAIL", 1)
        pdf.ln()
        total_obtained += sub["marks"]
        total_marks += sub["total_marks"]

    # Summary
    percentage = (total_obtained / total_marks) * 100
    grade = calculate_grade(total_obtained, total_marks)

    pdf.ln(5)
    pdf.cell(50, 8, f"Grand Total: {total_obtained} / {total_marks}", ln=True)
    pdf.cell(50, 8, f"Percentage: {percentage:.2f}%", ln=True)
    pdf.cell(50, 8, f"Grade: {grade}", ln=True)
    pdf.ln(10)

    # Signatures
    pdf.cell(90, 10, "Signature of Teacher", 0, 0)
    pdf.cell(90, 10, "Signature of Principal", 0, 1)

    pdf_file = "report_card.pdf"
    pdf.output(pdf_file)
    return pdf_file

# Streamlit UI
st.title("📜 Digital Student Report Card System")
st.subheader("Enter Student Details")

student_name = st.text_input("Student Name")
father_name = st.text_input("Father Name")
roll_no = st.text_input("Roll No")
student_class = st.selectbox("Class", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])

st.subheader("Enter Marks")

# Define subjects based on class
if student_class in ["1", "2", "3", "4", "5"]:
    subjects = [
        {"name": "English", "total_marks": 100},
        {"name": "Urdu", "total_marks": 100},
        {"name": "Math", "total_marks": 100},
        {"name": "Islamiat", "total_marks": 100},
        {"name": "General Knowledge", "total_marks": 50},
        {"name": "Computer", "total_marks": 75},
    ]
elif student_class in ["6", "7"]:
    subjects = [
        {"name": "English", "total_marks": 100},
        {"name": "Urdu", "total_marks": 100},
        {"name": "Math", "total_marks": 100},
        {"name": "Islamiat", "total_marks": 100},
        {"name": "Sindhi", "total_marks": 100},
        {"name": "Computer", "total_marks": 75},
    ]
else:
    subjects = [
        {"name": "English", "total_marks": 100},
        {"name": "Urdu", "total_marks": 100},
        {"name": "Math", "total_marks": 100},
        {"name": "Islamiat", "total_marks": 100},
        {"name": "Physics", "total_marks": 100},
        {"name": "Biology", "total_marks": 100},
        {"name": "Sindhi", "total_marks": 100},
        {"name": "Computer", "total_marks": 75},
    ]

# Collect Marks Input
for sub in subjects:
    sub["marks"] = st.number_input(f"Enter marks for {sub['name']} (Max: {sub['total_marks']})", min_value=0, max_value=sub["total_marks"], key=sub["name"])

# Generate PDF
if st.button("Generate Report Card"):
    if not student_name or not roll_no:
        st.error("⚠️ Please enter student details!")
    else:
        pdf_path = generate_pdf(student_name, father_name, roll_no, student_class, subjects)
        with open(pdf_path, "rb") as file:
            st.download_button("📥 Download Report Card", file, file_name="Report_Card.pdf", mime="application/pdf")

