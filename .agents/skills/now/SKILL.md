```markdown
# now Development Patterns

> Auto-generated skill from repository analysis

## Overview
```markdown
# now Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill summarizes the core development patterns and conventions used in the `now` repository. The repository is centered on Python and Markdown rather than TypeScript, so contributors should follow the conventions already present in the specific area they are modifying. When in doubt, prefer consistency with neighboring files over introducing new language- or framework-specific patterns.

## Coding Conventions

### File Naming
- Match the naming style already used by nearby files in the same directory.
- For documentation, use clear descriptive Markdown file names.
- For Python code, follow existing project patterns and standard Python naming conventions where applicable.

### Imports and Module Structure
- Follow the import style already used in the files you are editing.
- Use relative imports only when they are appropriate for the language and consistent with the local code.
- Avoid introducing new module structure conventions unless the surrounding code already uses them.

### Exports and Public APIs
- Preserve the public interface and organization patterns already used by the relevant package or module.

### Commit Message Patterns
- Commit messages are **freeform** and do not follow a strict prefix or type.
- Keep commit messages clear and concise.

## Workflows

### Adding a New Feature
**Trigger:** When implementing new functionality.
**Command:** `/add-feature`

1. Identify the language and directory conventions used by the feature area you are changing.
2. Create or modify files using the naming and organization patterns already present there.
3. Write code or documentation in a style consistent with neighboring files.
4. Add or update tests if the repository already includes tests for that area.
5. Update related documentation when behavior or usage changes.
6. Commit your changes with a clear, concise message.
7. Open a pull request for review.

### Writing Tests
**Trigger:** When adding or updating code that requires testing.
**Command:** `/write-test`

1. Look for existing test files near the code you are changing.
2. Follow the naming, framework, and organization patterns already used by those tests.
3. If no tests exist in that area, avoid inventing a new convention without checking the broader repository pattern.
4. Run the relevant tests and checks for the files you changed.
5. Commit the test updates alongside your implementation.

### Refactoring Code
**Trigger:** When improving or restructuring existing code.
**Command:** `/refactor`

1. Identify the code or documentation to refactor.
2. Preserve behavior while making the structure more consistent with local repository patterns.
3. Update imports, references, and related documentation as needed.
4. Update or add tests following the existing conventions in that area.
5. Commit changes with a descriptive message.

## Testing Patterns

- Follow the structure and naming of existing test files in the part of the repository you are modifying.
- The specific testing framework is not declared in this skill; use the framework already present in the repository.
- Place tests alongside or near the code they verify if that matches the existing project layout.
- For documentation-only changes, verify rendered output and links where practical.

## Commands
| Command        | Purpose                                               |
|----------------|-------------------------------------------------------|
| /add-feature   | Start the process for adding a new feature            |
| /write-test    | Guide for writing and organizing tests                |
| /refactor      | Steps for refactoring code or documentation           |

## Coding Conventions

### File Naming
- Use **camelCase** for file names.
  - Example: `myFeature.ts`, `userProfile.ts`

### Import Style
- Use **relative imports** for modules within the project.
  - Example:
    ```typescript
    import { fetchData } from './apiUtils';
    ```

### Export Style
- Use **named exports** rather than default exports.
  - Example:
    ```typescript
    // In userProfile.ts
    export function getUserProfile(id: string) { ... }
    
    // In another file
    import { getUserProfile } from './userProfile';
    ```

### Commit Message Patterns
- Commit messages are **freeform** and do not follow a strict prefix or type.
- Average commit message length is ~29 characters.

## Workflows

### Adding a New Feature
**Trigger:** When implementing a new functionality.
**Command:** `/add-feature`

1. Create a new file using camelCase naming (e.g., `newFeature.ts`).
2. Write your TypeScript code, using named exports.
3. Use relative imports to include any dependencies.
4. Add corresponding tests in a `.test.ts` file.
5. Commit your changes with a clear, concise message.
6. Open a pull request for review.

### Writing Tests
**Trigger:** When adding or updating code that requires testing.
**Command:** `/write-test`

1. Create a test file with the pattern `*.test.ts` (e.g., `apiUtils.test.ts`).
2. Write tests for your functions or modules.
3. Use the project's testing framework (unknown, but follow existing patterns).
4. Run tests to ensure correctness.
5. Commit the test file alongside your implementation.

### Refactoring Code
**Trigger:** When improving or restructuring existing code.
**Command:** `/refactor`

1. Identify the code to refactor.
2. Update file and variable names to match camelCase conventions.
3. Ensure all imports are relative and exports are named.
4. Update or add tests as needed.
5. Commit changes with a descriptive message.

## Testing Patterns

- Test files use the pattern `*.test.ts`.
- The specific testing framework is not detected; follow the structure of existing test files.
- Place tests alongside or near the modules they test.
- Example test file name: `userProfile.test.ts`

## Commands
| Command        | Purpose                                      |
|----------------|----------------------------------------------|
| /add-feature   | Start the process for adding a new feature   |
| /write-test    | Guide for writing and organizing tests       |
| /refactor      | Steps for refactoring code                   |
```
