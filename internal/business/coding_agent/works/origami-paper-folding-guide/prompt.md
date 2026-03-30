I need you to create an origami instruction generator that can produce step-by-step folding guides for different paper models.

The system should:
1. Complete the implementation of the origami_models.py module by filling in the missing functions
2. Create a command-line script origami_generator.py that uses the origami_models module
3. Support at least 4 models: crane, frog, boat, and butterfly
4. Generate detailed step-by-step folding instructions (at least 5 steps per model, 15+ for crane)
5. Save instructions to text files named after the model (e.g., "crane_instructions.txt")

The origami_models.py module needs these functions implemented:
- get_available_models(): return list of available model names
- generate_instructions(model_name): return list of instruction steps
- save_instructions_to_file(model_name, instructions): save numbered instructions to file

Requirements for instruction files:
- Files should be saved with numbered steps (1., 2., 3., etc.)
- File content should be substantial (over 100 characters)
- Files should reference the model name (e.g., "crane" in crane_instructions.txt)
- Instructions should contain realistic origami terminology (fold, crease, valley, mountain, paper, corner, edge)

The CLI script should handle user input properly and create instruction files when run.