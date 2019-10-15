import argparse
import jsonlines

def parse_answer(document_text, answer_candidate):
    tokens = document_text.split(' ')
    start  = answer_candidate['start_token']
    end    = answer_candidate['end_token']
    return ' '.join(tokens[start:end])

def process_nq_data(in_path, out_path='nq_data.txt', limit=float('inf'), append=False):
    """Exports simplified NQ data as a .txt file,
    with answers and questions on alternating lines.
    """
    write_mode = 'a' if append else 'w'
    with jsonlines.open(in_path) as reader, open(out_path, write_mode) as writer:
        questions_written = 0
        for q_data in reader:
            # question
            q_text = q_data['question_text'].strip()
            if not q_text.endswith('?'):
                q_text += '?'
            if not q_text[0].isupper():
                q_text = q_text[0].upper() + q_text[1:]
            # answer
            annotations = q_data['annotations']
            answer_candidates = q_data['long_answer_candidates']
            answer = ''
            if len(annotations) > 0:
                annotation = annotations[0]
                answer = parse_answer(q_data['document_text'], annotation['long_answer'])
            elif len(answer_candidates) > 0:
                answer = parse_answer(q_data['document_text'], answer_candidates[-1])
            if answer.startswith('<P>'):
                # only accept paragraph answers
                answer = answer.replace('<P>', '').replace('</P>', '')
                # strip to single sentence
                answer = answer[:answer.find('.')+1].strip()
                # get rid of some of the spaces around punctuation
                answer = answer.replace('`` ', '"')
                answer = answer.replace(" ''", '"')
                for char in ('(',):
                    answer = answer.replace(char + ' ', char)
                for char in ('.', "'", ';', ')', ','):
                    answer = answer.replace(' ' + char, char)
                if len(answer) > 1:
                    writer.write('%s\n%s\n' % (answer, q_text))  # answer-question
                    questions_written += 1
                    if questions_written % 10000 == 0:
                        print('[o] %d questions written' % questions_written)
                    if questions_written >= limit:
                        break
    indicator = '+' if questions_written > 0 else '-'
    print('[%s] wrote %d questions to %s' % (indicator, questions_written, out_path))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('in_path', type=str, help='path to simplified NQ data')
    parser.add_argument('--out_path', '-o', type=str, help='output_path', default='nq_data.txt')
    parser.add_argument('--limit', '-l', type=int, help='max number of questions to include', default=-1)
    parser.add_argument('--append', '-a', action='store_true')
    args = parser.parse_args()
    if args.limit == -1:
        args.limit = float('inf')
    process_nq_data(args.in_path, args.out_path, args.limit, args.append)
