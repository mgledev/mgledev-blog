def clean_text(text):
    return text.replace('\n', ' ').replace('  ', ' ').strip()

def correct_text(text):
    # Przykładowe poprawki (można rozbudować)
    corrections = {
        'studentuw': 'studentów',
        'cwiczen': 'ćwiczeń',
        'celu': 'celu',
    }
    for wrong, right in corrections.items():
        text = text.replace(wrong, right)
    return text

def summarize(text):
    lines = text.split('. ')
    return '. '.join(lines[:2]) + '...' if len(lines) > 2 else text
