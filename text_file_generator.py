import os
from datetime import datetime
from textwrap import wrap

def create_text_file(content_list, output_file='output/lecture_notes.txt'):
    """Generate concise notes for short videos"""
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("CONCISE VIDEO NOTES\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write("="*40 + "\n\n")
            
            for i, content in enumerate(content_list, 1):
                # Skip very short sections
                if len(content.split()) < 4:
                    continue
                    
                f.write(f"Key Point {i}:\n")
                f.write("-"*40 + "\n")
                
                # Clean paragraph formatting
                paragraph = ' '.join(content.split())
                for line in wrap(paragraph, width=70):
                    f.write(line + "\n")
                
                f.write("\n")
            
            f.write("="*40 + "\n")
            f.write("End of notes\n")
        
        return output_file
    except Exception as e:
        print(f"Error creating notes: {e}")
        return None
    