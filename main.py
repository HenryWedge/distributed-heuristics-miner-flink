import os
from dotenv import load_dotenv

if __name__ == '__main__':
    precision_token_based_replay = 0.045
    fitness_token_based_replay = 0.3223
    precision_alignments = 0.777
    fitness_alignments = 0.656
    print(f"""precision_token_based_replay {precision_token_based_replay}
fitness_token_based_replay {fitness_token_based_replay}
precision_alignments {precision_alignments}
fitness_alignments {fitness_alignments}
""")
