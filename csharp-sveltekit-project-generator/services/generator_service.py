import os
import shutil
import uuid
import jinja2
from helpers.util import lower_first_letter
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
    _generate_repositories(output_path, project_name, classes, env)
    _generate_services(output_path, project_name, classes, env)
    _generate_controllers(output_path, project_name, classes, env)
    _generate_dtos(output_path, project_name, classes, env)
    _generate_service_extensions(output_path, project_name, classes, env)


def generate_web_app(output_path: str, project_name: str, classes: list[EntityClass]):
    project_name = project_name.lower()
    output_path = os.path.join(output_path, project_name)
    _generate_structure(WEB_APP_STATIC_SOURCE_FOLDER, output_path, project_name)

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(WEB_APP_DYNAMIC_TEMPLATES_FOLDER)
    )

    env.filters['lower_first_letter'] = lower_first_letter

    _generate_main_page(output_path, project_name, classes, env)
    _generate_profile_pages(output_path, project_name, classes, env)
    _generate_list_pages(output_path, project_name, classes, env)
    _generate_mappers(output_path, project_name, classes, env)


def _generate_structure(source_path: str, output_path: str, project_name: str, is_api: bool = False):
    print(f"{"API" if is_api else "WebAPP" }: Generating project structure for {project_name}...")
    context = {
        "project_name": project_name,
        "context_name": project_name.split(".")[0],
        "database_name": project_name.split(".")[0],
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
        os.makedirs(f"{output_path}/src/routes/{entity_class.name.lower()}/profile", exist_ok=True)
        rendered_content = template.render(entity_class.get_context(project_name))
        output_file_path = os.path.join(
            output_path, "src/routes", entity_class.name.lower(), "profile", "+page.svelte"
        )
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(rendered_content)
    
    print(f"WebAPP: All profile pages for {project_name} processed successfully.")

def _generate_list_pages(output_path: str, project_name: str, classes: list[EntityClass], env: jinja2.Environment):
    print(f"WebAPP: Generating list pages for {project_name}...")
    template = env.get_template("list_page_template.jinja")

    for entity_class in classes:
        os.makedirs(f"{output_path}/src/routes/{entity_class.name.lower()}/list", exist_ok=True)
        rendered_content = template.render(entity_class.get_context(project_name))

        output_file_path = os.path.join(
            output_path, "src/routes", entity_class.name.lower(), "list", "+page.svelte"
        )
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(rendered_content)
    
    print(f"WebAPP: All list pages for {project_name} processed successfully.")


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

def _generate_repositories(output_path: str, project_name: str, classes: list[EntityClass], env: jinja2.Environment):
    print(f"API: Generating repositories for {project_name}...")
    repository_template = env.get_template("repository_template.jinja")
    interface_template = env.get_template("repository_interface_template.jinja")

    os.makedirs(f"{output_path}/Application/Repositories", exist_ok=True)
    os.makedirs(f"{output_path}/Infrastructure/Repositories", exist_ok=True)

    for entity_class in classes:
        rendered_repository_content = repository_template.render(entity_class.get_context(project_name))
        rendered_interface_content = interface_template.render(entity_class.get_context(project_name))

        interface_output_file_path = os.path.join(
            output_path, "Application", "Repositories",  f"I{entity_class.name}Repository.cs"
        )

        repository_output_file_path = os.path.join(
            output_path, "Infrastructure", "Repositories",  f"{entity_class.name}Repository.cs"
        )

        with open(repository_output_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(rendered_repository_content)

        with open(interface_output_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(rendered_interface_content)

    print(f"API: All repository files for {project_name} processed successfully.")

def _generate_services(output_path: str, project_name: str, classes: list[EntityClass], env: jinja2.Environment):
    print(f"API: Generating services for {project_name}...")
    service_template = env.get_template("service_template.jinja")
    interface_template = env.get_template("service_interface_template.jinja")

    os.makedirs(f"{output_path}/Application/Services", exist_ok=True)
    os.makedirs(f"{output_path}/Infrastructure/Services", exist_ok=True)

    for entity_class in classes:
        rendered_service_content = service_template.render(entity_class.get_context(project_name))
        rendered_interface_content = interface_template.render(entity_class.get_context(project_name))

        interface_output_file_path = os.path.join(
            output_path, "Application", "Services",  f"I{entity_class.name}Service.cs"
        )

        service_output_file_path = os.path.join(
            output_path, "Infrastructure", "Services",  f"{entity_class.name}Service.cs"
        )

        with open(service_output_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(rendered_service_content)

        with open(interface_output_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(rendered_interface_content)

    print(f"API: All services files for {project_name} processed successfully.")

def _generate_controllers(output_path: str, project_name: str, classes: list[EntityClass], env: jinja2.Environment):
    print(f"API: Generating controllers for {project_name}...")
    controller_template = env.get_template("controller_template.jinja")

    os.makedirs(f"{output_path}/Controllers", exist_ok=True)

    for entity_class in classes:
        rendered_controller_content = controller_template.render(entity_class.get_context(project_name))

        controller_output_file_path = os.path.join(
            output_path, "Controllers", f"{entity_class.name}Controller.cs"
        )

        with open(controller_output_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(rendered_controller_content)

    print(f"API: All controllers files for {project_name} processed successfully.")

def _generate_dtos(output_path: str, project_name: str, classes: list[EntityClass], env: jinja2.Environment):
    print(f"API: Generating requests for {project_name}...")
    request_template = env.get_template("request_template.jinja")
    response_template = env.get_template("response_template.jinja")
    mapping_profile_template = env.get_template("mapping_profile_template.jinja")

    os.makedirs(f"{output_path}/Data/Requests", exist_ok=True)
    os.makedirs(f"{output_path}/Data/Responses", exist_ok=True)
    os.makedirs(f"{output_path}/Infrastructure/MappingProfiles", exist_ok=True)

    for entity_class in classes:
        rendered_request_content = request_template.render(entity_class.get_context(project_name))
        rendered_response_content = response_template.render(entity_class.get_context(project_name))
        rendered_mapping_profile_content = mapping_profile_template.render(entity_class.get_context(project_name))

        requests_output_file_path = os.path.join(
            output_path, "Data", "Requests", f"{entity_class.name}Request.cs"
        )

        responses_output_file_path = os.path.join(
            output_path, "Data", "Responses", f"{entity_class.name}Response.cs"
        )

        mapping_profile_output_file_path = os.path.join(
            output_path, "Infrastructure", "MappingProfiles", f"{entity_class.name}Response.cs"
        )

        with open(requests_output_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(rendered_request_content)

        with open(responses_output_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(rendered_response_content)

        with open(mapping_profile_output_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(rendered_mapping_profile_content)

    print(f"API: All dtos files for {project_name} processed successfully.")
    

def _generate_service_extensions(output_path: str, project_name: str, classes: list[EntityClass], env: jinja2.Environment):
    print(f"API: Generating service extensions for {project_name}...")
    template = env.get_template("service_extension_template.jinja")

    os.makedirs(f"{output_path}/Infrastructure/Extensions", exist_ok=True)

    context = {
        'project_name': project_name,
        'context_name': project_name.split('.')[0],
        'classes': [{
            'name': cls.name,
            'plural_name': cls.get_plural_name(),
        } for cls in classes]
    }

    rendered_content = template.render(context)

    output_file_path = os.path.join(output_path, "Infrastructure", "Extensions", "ServiceExtensions.cs")
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write(rendered_content)

    print(f"API: All service extensions files for {project_name} processed")

def _generate_main_page(output_path: str, project_name: str, classes: list[EntityClass], env: jinja2.Environment):
    print(f"WebAPP: Generating main page for {project_name}...")
    template = env.get_template("main_page_template.jinja")

    os.makedirs(f"{output_path}/src/routes", exist_ok=True)

    rendered_content = template.render({
        'project_name': project_name,
        'context_name': project_name.split('.')[0],
        'classes': [{
            'name': cls.name,
            'plural_name': cls.get_plural_name(),
        } for cls in classes]
    })

    output_file_path = os.path.join(output_path, "src", "routes", "+page.svelte")
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write(rendered_content)

    print(f"WebAPP: Main page for {project_name} processed successfully.")

def _generate_mappers(output_path: str, project_name: str, classes: list[EntityClass], env: jinja2.Environment):
    print(f"API: Generating mappers for {project_name}...")
    mapper_template = env.get_template("mapper_template.jinja")

    os.makedirs(f"{output_path}/src/lib/helpers", exist_ok=True)

    rendered_content = mapper_template.render({
        'project_name': project_name,
        'context_name': project_name.split('.')[0],
        'classes': [cls.get_context(project_name) for cls in classes]
    })

    output_file_path = os.path.join(output_path, "src", "lib", "helpers", "mappers.ts")

    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write(rendered_content)

    print(f"WebAPP: Mappers for {project_name} processed successfully.")
