```markdown
# now Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill teaches the core development patterns and conventions used in the `now` TypeScript codebase. It covers file organization, code style, import/export practices, and testing patterns. By following these guidelines, contributors can write consistent, maintainable code and effectively collaborate on the project.

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
