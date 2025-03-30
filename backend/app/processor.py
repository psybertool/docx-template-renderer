from docxtpl import DocxTemplate

def process_template(template_path: str, variables: dict, output_path: str):
    doc = DocxTemplate(template_path)
    doc.render(variables)
    doc.save(output_path)

def extract_variables(template_path: str) -> list:
    doc = DocxTemplate(template_path)
    return sorted(list(doc.get_undeclared_template_variables()))

