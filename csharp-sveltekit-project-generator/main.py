import argparse
import services.parser_service as parser_service
import services.generator_service as generator_service


def main():
    # Create the parser
    parser = argparse.ArgumentParser(
        description="Script to generate project components."
    )

    # Add the arguments
    parser.add_argument(
        "--project_name",
        type=str,
        default="Library",
        help="Specify the name of the project (default: Library)",
    )

    parser.add_argument(
        "--generate",
        type=str,
        choices=["back", "front", "all"],
        default="all",
        help="Specify what to generate: back, front, or all (default: all)",
    )

    parser.add_argument(
        "--model_path",
        type=str,
        default="csharp-sveltekit-project-generator/resources/LibraryModel.xml",
        help="Path to the model XML file (default: csharp-sveltekit-project-generator/resources/LibraryModel.xml)",
    )

    parser.add_argument(
        "--output_path",
        type=str,
        default="output",
        help="Path to the output folder (default: output)",
    )

    # Parse the arguments
    args = parser.parse_args()

    # Use the arguments
    print("Generating project with provided arguments:")
    print(f"Project Name: {args.project_name}")
    print(f"Generate: {args.generate}")
    print(f"Model Path: {args.model_path}")
    print(f"Output Path: {args.output_path}")

    parser_service.parse(args.model_path)
    generator_service.generate_api(args.output_path, args.project_name)
    generator_service.generate_web_app(args.output_path, args.project_name)


if __name__ == "__main__":
    main()
