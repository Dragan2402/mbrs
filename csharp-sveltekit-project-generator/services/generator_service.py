import os
import shutil
import uuid
import jinja2

API_STATIC_SOURCE_FOLDER = "csharp-sveltekit-project-generator/templates/api/static"
WEB_APP_STATIC_SOURCE_FOLDER = (
    "csharp-sveltekit-project-generator/templates/webApp/static"
)


def generate_api(output_path: str, project_name: str):
    project_name = project_name + ".API"
    output_path = os.path.join(output_path, project_name)
    _generate_structure(API_STATIC_SOURCE_FOLDER, output_path, project_name)


def generate_web_app(output_path: str, project_name: str):
    project_name = project_name.lower()
    output_path = os.path.join(output_path, project_name)
    _generate_structure(WEB_APP_STATIC_SOURCE_FOLDER, output_path, project_name)


def _generate_structure(source_path: str, output_path: str, project_name: str):
    print(f"Generating project structure for {project_name}...")
    context = {
        "project_name": project_name,
        "project_id": _generate_random_project_id(),
    }

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(source_path))

    os.makedirs(output_path, exist_ok=True)

    for root, _, files in os.walk(source_path):
        for file_name in files:
            if "{{project_name}}" in file_name:
                new_file_name = file_name.replace("{{project_name}}", project_name)
            else:
                new_file_name = file_name

            file_path = os.path.join(root, file_name)

            relative_dir = os.path.relpath(root, source_path)
            output_dir = os.path.join(output_path, relative_dir)

            os.makedirs(output_dir, exist_ok=True)

            if file_name.endswith(".jinja"):
                output_file_name = new_file_name[:-6]

                template_path = os.path.join(relative_dir, file_name).replace("\\", "/")

                template = env.get_template(template_path)
                rendered_content = template.render(context)

                output_file_path = os.path.join(output_dir, output_file_name)
                with open(output_file_path, "w", encoding="utf-8") as output_file:
                    output_file.write(rendered_content)
            else:
                output_file_path = os.path.join(output_dir, new_file_name)
                shutil.copy(file_path, output_file_path)

    print(f"All static files for {project_name} processed successfully.")


def _generate_random_project_id():
    return str(uuid.uuid4())
