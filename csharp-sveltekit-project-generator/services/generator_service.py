import os
import shutil
import uuid
import jinja2
from domain.entity_class import EntityClass

API_STATIC_SOURCE_FOLDER = "csharp-sveltekit-project-generator/templates/api/static"
WEB_APP_STATIC_SOURCE_FOLDER = (
    "csharp-sveltekit-project-generator/templates/webApp/static"
)
API_DYNAMIC_TEMPLATES_FOLDER = (
    "csharp-sveltekit-project-generator/templates/api/dynamic"
)

WEB_APP_DYNAMIC_TEMPLATES_FOLDER = (
"csharp-sveltekit-project-generator/templates/webApp/dynamic" 
)

def generate_api(output_path: str, project_name: str, classes: list[EntityClass]):
    project_name = project_name + ".API"
    output_path = os.path.join(output_path, project_name)

    _generate_structure(API_STATIC_SOURCE_FOLDER, output_path, project_name, True)

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(API_DYNAMIC_TEMPLATES_FOLDER)
    )
    _generate_domain(output_path, project_name, classes, env)
    _generate_db_context(output_path, project_name, classes, env)


def generate_web_app(output_path: str, project_name: str, classes: list[EntityClass]):
    project_name = project_name.lower()
    output_path = os.path.join(output_path, project_name)
    _generate_structure(WEB_APP_STATIC_SOURCE_FOLDER, output_path, project_name)

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(WEB_APP_DYNAMIC_TEMPLATES_FOLDER)
    )
    _generate_profile_pages(output_path, project_name, classes, env)


def _generate_structure(source_path: str, output_path: str, project_name: str, is_api: bool = False):
    print(f"{"API" if is_api else "WebAPP" }: Generating project structure for {project_name}...")
    context = {
        "project_name": project_name,
        "context_name": project_name.split(".")[0],
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

                template = env.get_template(template_path, project_name)
                rendered_content = template.render(context)

                output_file_path = os.path.join(output_dir, output_file_name)
                with open(output_file_path, "w", encoding="utf-8") as output_file:
                    output_file.write(rendered_content)
            else:
                output_file_path = os.path.join(output_dir, new_file_name)
                shutil.copy(file_path, output_file_path)

    print(f"{"API" if is_api else "WebAPP" }: All static files for {project_name} processed successfully.")


def _generate_random_project_id():
    return str(uuid.uuid4())


def _generate_domain(output_path: str, project_name: str, classes: list[EntityClass], env: jinja2.Environment):
    print(f"API: Generating domain for {project_name}...")
    template = env.get_template("class_template.jinja")

    os.makedirs(f"{output_path}/Domain", exist_ok=True)

    for entity_class in classes:
        rendered_content = template.render(entity_class.get_context(project_name))
        output_file_path = os.path.join(
            output_path, "Domain", f"{entity_class.name}.cs"
        )
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(rendered_content)

    print(f"API: All domain files for {project_name} processed successfully.")

def _generate_profile_pages(output_path: str, project_name: str, classes: list[EntityClass], env: jinja2.Environment):
    print(f"WebAPP: Generating profile pages for {project_name}...")
    template = env.get_template("profile_page_template.jinja")

    for entity_class in classes:
        os.makedirs(f"{output_path}/src/routes/{entity_class.get_plural_name().lower()}/profile", exist_ok=True)
        rendered_content = template.render(entity_class.get_context(project_name))
        output_file_path = os.path.join(
            output_path, "src/routes", entity_class.get_plural_name().lower(), "profile", "+page.svelte"
        )
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(rendered_content)
    
    print(f"WebAPP: All profile pages for {project_name} processed successfully.")

    
def _generate_db_context(output_path: str, project_name: str, classes: list[EntityClass], env: jinja2.Environment):
    context = {
        'project_name': project_name,
        'context_name': project_name.split('.')[0],
        'classes': [{
            'name': cls.name,
            'plural_name': cls.get_plural_name(),
        } for cls in classes]
    }
    print(f"Generating db context for {project_name}...")
    template = env.get_template("db_context_template.jinja")
    rendered_content = template.render(context)

    os.makedirs(f"{output_path}/Data", exist_ok=True)

    output_file_path = os.path.join(output_path, "Data", "AppDbContext.cs")
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write(rendered_content)

    print(f"API: All db context files for {project_name} processed successfully.")
