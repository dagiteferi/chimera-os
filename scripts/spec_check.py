import os
import json
import sys


SPEC_FILES = [
    "specs/_meta.md",
    "specs/functional.md",
    "specs/technical.md",
    "specs/openclaw_integration.md",
]

SKILLS = [
    "trend_fetcher",
    "content_generator",
    "engagement_manager",
]

TEST_FILES = [
    "tests/test_trend_fetcher.py",
    "tests/test_skills_interface.py",
]

# --- Main Validation Logic ---
def main():
    """
    Runs all validation checks and reports the final status.
    Exits with 1 if any check fails, 0 otherwise.
    """
    print("--- Running Chimera Specification Validation ---")
    checks = {
        "Spec Files": check_spec_files,
        "Skill Schemas": check_skill_schemas,
        "Test File Spec References": check_test_file_references,
        "Spec Meta References": check_spec_meta_references,
    }

    all_passed = True
    for name, check_func in checks.items():
        print(f"\n[CHECKING] {name}...")
        if not check_func():
            all_passed = False
            print(f"[FAILED] {name} check failed.")
        else:
            print(f"[PASSED] {name} check successful.")

    print("\n--- Validation Summary ---")
    if all_passed:
        print("All specification checks passed successfully!")
        sys.exit(0)
    else:
        print("One or more specification checks failed. Please review the errors above.")
        sys.exit(1)

# --- Individual Check Functions ---

def check_spec_files():
    """Checks if all required spec files exist."""
    passed = True
    for f in SPEC_FILES:
        if not os.path.exists(f):
            print(f"  ERROR: Missing spec file: {f}")
            passed = False
        else:
            print(f"  OK: Found {f}")
    return passed

def check_skill_schemas():
    """
    Checks for the existence and validity of input/output JSON schemas for each skill.
    Ref: skills/*/input_schema.json, skills/*/output_schema.json
    """
    passed = True
    for skill in SKILLS:
        skill_path = os.path.join("skills", skill)
        if not os.path.isdir(skill_path):
            print(f"  ERROR: Missing skill directory: {skill_path}")
            passed = False
            continue

        for schema_type in ["input_schema.json", "output_schema.json"]:
            schema_path = os.path.join(skill_path, schema_type)
            if not os.path.exists(schema_path):
                print(f"  ERROR: Missing schema file: {schema_path}")
                passed = False
                continue
            
            # Check if JSON is valid
            try:
                with open(schema_path, 'r') as f:
                    data = json.load(f)
                print(f"  OK: Valid JSON in {schema_path}")
                
                # Basic structure validation
                # Ref: specs/technical.md (API Contracts)
                if schema_type == "input_schema.json":
                    if not ("skill_name" in data and "parameters" in data):
                        print(f"  ERROR: Invalid structure in {schema_path}. Missing 'skill_name' or 'parameters'.")
                        passed = False
                else: # output_schema.json
                    if not any(key in data for key in ["trends", "content", "interaction"]):
                         print(f"  ERROR: Invalid structure in {schema_path}. Missing primary output key.")
                         passed = False

            except json.JSONDecodeError as e:
                print(f"  ERROR: Invalid JSON in {schema_path}: {e}")
                passed = False
    return passed

def check_test_file_references():
    """
    Checks if test files contain references to the specification documents.
    This enforces traceability between tests and requirements.
    """
    passed = True
    keywords = ["SRS Section", "technical.md", "functional.md"]
    for test_file in TEST_FILES:
        if not os.path.exists(test_file):
            print(f"  ERROR: Test file not found: {test_file}")
            passed = False
            continue
        
        with open(test_file, 'r') as f:
            content = f.read()
            if not any(keyword in content for keyword in keywords):
                print(f"  ERROR: No spec reference found in {test_file}. Please add a docstring or comment referencing the spec.")
                passed = False
            else:
                print(f"  OK: Found spec reference in {test_file}")
    return passed

def check_spec_meta_references():
    """
    Checks if the meta spec file references key project documents.
    Ref: specs/_meta.md
    """
    passed = True
    meta_file = "specs/_meta.md"
    keywords = ["SRS", "Task 1 Report"]
    
    if not os.path.exists(meta_file):
        print(f"  ERROR: Meta spec file not found: {meta_file}")
        return False

    with open(meta_file, 'r') as f:
        content = f.read()
        for keyword in keywords:
            if keyword not in content:
                print(f"  ERROR: Missing reference to '{keyword}' in {meta_file}")
                passed = False
            else:
                print(f"  OK: Found reference to '{keyword}' in {meta_file}")
    return passed

if __name__ == "__main__":
    main()
