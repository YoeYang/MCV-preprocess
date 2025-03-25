import os

def check_speaker_pattern(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    if len(lines) < 2:
        return None

    speakers = [line.split()[1] for line in lines]

    player = speakers[-1]

    # 1. check whether the first line is player
    if speakers[0] == player:
        return filename

    # 2. find all player's line
    player_indices = [i for i, speaker in enumerate(speakers) if speaker == player]

    # 3. check whether player and interviewer appear alternately
    for i in range(1, len(player_indices)):
        if player_indices[i] - player_indices[i-1] != 2:
            return filename

    return None

def check_files_in_directory(directory):
    invalid_files = []
    for filename in os.listdir(directory):
        print("checking:" + filename)
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            result = check_speaker_pattern(file_path)
            if result:
                invalid_files.append(filename)

    # output file name which is not qualified
    if invalid_files:
        sorted_invalid_files = sorted(invalid_files, key=lambda x: int(x.split('.')[0]))
        print("Wrong file:")
        print(len(sorted_invalid_files))
        for file in sorted_invalid_files:
            print(file)
    else:
        print("All files are qualified!")

# 调用示例
directory = './data-merge'  # edit to your merge file
check_files_in_directory(directory)
