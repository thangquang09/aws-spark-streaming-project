import re
from datetime import datetime

def extract_job_title(file_content):
    file_content = file_content.strip()
    job_title = file_content.split("\n")[0]
    return job_title

def extract_salary_start(file_content):
    try:
        pattern = r'Mức lương:\s*(\d+\s*triệu|\d+\s*-\s*\d+\s*triệu|Thỏa thuận)'
        salary = re.findall(pattern, file_content, re.IGNORECASE)
        
        if " - " in salary[0]:
            return str(int(salary[0].split(" - ")[0]) * 1e6)
        elif "thỏa thuận" in salary[0].lower():
            return "Thỏa thuận"
        else:
            return salary[0]

    except Exception as e:
        raise ValueError(f"Error extracting salary start: {e}")

def extract_salary_end(file_content):
    try:
        pattern = r'Mức lương:\s*(\d+\s*triệu|\d+\s*-\s*\d+\s*triệu|Thỏa thuận)'
        salary = re.findall(pattern, file_content, re.IGNORECASE)
        
        if " - " in salary[0]:
            tmp = salary[0].split(" - ")[1]
            number = re.findall(r'\d+', tmp)[0]
            return str(int(number) * 1e6)
        elif "thỏa thuận" in salary[0].lower():
            return "Thỏa thuận"
        else:
            return salary[0]

    except Exception as e:
        raise ValueError(f"Error extracting salary end: {e}")

def extract_experience(file_content):
    try:
        pattern = r'Kinh nghiệm:\s*(\d+\s*năm)'
        experience = re.findall(pattern, file_content, re.IGNORECASE)
        if experience:
            return experience[0]
        else:
            file_content = file_content.strip()
            experience = file_content.split("\n")[3].split(": ")[1]
            return experience
    except Exception as e:
        raise ValueError(f"Error extracting experience: {e}")

def extract_submission_deadline(file_content):
    try:
        file_content = file_content.strip()
        deadline = file_content.split("\n")[4].split(": ")[1]
        if "-" in deadline:
            deadline = deadline.replace("-", "/")
        deadline = datetime.strptime(deadline, "%d/%m/%Y")
        return deadline
    except Exception as e:
        raise ValueError(f"Error extracting submission deadline: {e}")


def extract_job_description(file_content):
    try:
        pattern = r'MÔ TẢ CÔNG VIỆC\n(.*?)(?=\nYÊU CẦU ỨNG VIÊN)'
        description = re.search(pattern, file_content, re.DOTALL)
        return description.group(1)
    except Exception as e:
        raise ValueError(f"Error extracting job description: {e}")

def extract_job_requirements(file_content):
    try:
        pattern = r'YÊU CẦU ỨNG VIÊN\n(.*?)(?=\nQUYỀN LỢI)'
        requirements = re.search(pattern, file_content, re.DOTALL)
        return requirements.group(1)
    except Exception as e:
        raise ValueError(f"Error extracting job requirements: {e}")

def extract_benefits(file_content):
    try:
        pattern = r'QUYỀN LỢI\n(.*?)(?=\nĐỊA ĐIỂM LÀM VIỆC)'
        benefits = re.search(pattern, file_content, re.DOTALL)
        return benefits.group(1)
    except Exception as e:
        raise ValueError(f"Error extracting benefits: {e}")

def extract_company_address(file_content):
    try:
        pattern = r'ĐỊA ĐIỂM LÀM VIỆC\n(.*)'
        address = re.search(pattern, file_content, re.DOTALL)
        return address.group(1)
    except Exception as e:
        raise ValueError(f"Error extracting address: {e}")
        