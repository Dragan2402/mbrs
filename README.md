# MBRS

# Description

This project represents python parser/generator to create .NET API and SvelteKit projects ecosystem. Where .NET API represents backend side and SvelteKit frontend part of the solution.
Domain model can be defined in MagicDraw and provided to the generator, all the existing magic draw examples can be fined inside resources folder.

# Startup

Create virtual environment and install the required packages.
Run the main.py python file, it accepts 4 arguments:

1. Project name Specify the name of the project (default: Library)
2. Generation option choices=back, front, all (Default)
3. Model xml file path
4. Output folder path

# Steps needed after generation

To have a nice and functional system these things need to be done after generating output:

For WebApp

1. Run `npm install`
2. Run `npx swagger-typescript-api@12.0.4 -p https://localhost:7159/swagger/v1/swagger.json -o ./src/lib/api -n apiV1.ts --module-name-index 1 -t swagger-templates/` to generate request library (change port according to Api port)

For API

1. Create initial migration `Add-Migration Initial`
2. Also you can run Analyzer and Cleanup to format code
