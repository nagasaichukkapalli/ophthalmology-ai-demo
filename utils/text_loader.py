import re

class TextLoader:
    @staticmethod
    def load_diseases(filepath):
        """
        Parses the eye_diseases.txt file.
        Expected format:
        Disease: Name
        Symptoms: ...
        Description: ...
        Specialist: ...
        """
        diseases = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split by double newline which seems to separate entries
            blocks = content.strip().split('\n\n')
            
            for block in blocks:
                disease = {}
                lines = block.split('\n')
                for line in lines:
                    if line.startswith('Disease:'):
                        disease['name'] = line.replace('Disease:', '').strip()
                    elif line.startswith('Symptoms:'):
                        disease['symptoms'] = line.replace('Symptoms:', '').strip()
                    elif line.startswith('Description:'):
                        disease['description'] = line.replace('Description:', '').strip()
                    elif line.startswith('Specialist:'):
                        disease['specialist'] = line.replace('Specialist:', '').strip()
                
                if 'name' in disease:
                    diseases.append(disease)
                    
        except FileNotFoundError:
            print(f"Error: File {filepath} not found.")
            return []
            
        return diseases

    @staticmethod
    def load_guidelines(filepath):
        """Loads reference guidelines for freshness check."""
        guidelines = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        guidelines.append(line.strip())
        except FileNotFoundError:
            return []
        return guidelines
