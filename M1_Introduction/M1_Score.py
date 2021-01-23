import argparse
import wer
import re


def score(ref_trn=None, hyp_trn=None):
    reference_string = ""
    hypothesis_string = ""
    num_sentences = 0
    num_words = 0
    num_sentences_error = 0
    num_deletions = 0
    num_insertions = 0
    num_substitutions = 0
    num_errors = 0
    with open(ref_trn) as reference, open(hyp_trn) as hypothesis:
        for lineR, lineH in zip(reference, hypothesis):
            num_sentences += 1

            id_pattern = re.compile(r'\(.+\)')

            id_ref_match = id_pattern.search(lineR)
            reference_string = lineR[:id_ref_match.start()]

            id_hyp_match = id_pattern.search(lineH)
            hypothesis_string = lineH[:id_hyp_match.start()]

            ref_word_list = reference_string.split()
            hyp_word_list = hypothesis_string.split()

            num_words += len(reference_string.split())
            #print(reference_string + id_ref_match[0])
            #print(hypothesis_string + id_hyp_match[0])

            tokens, edits, deletions, insertions, substitutions = wer.string_edit_distance(
                ref=ref_word_list, hyp=hyp_word_list)
            if deletions != 0 or insertions != 0 or substitutions != 0:
                num_sentences_error += 1
            num_errors += edits
            num_deletions += deletions
            num_insertions += insertions
            num_substitutions += substitutions

            print(f'''id: {id_ref_match[0]}
Scores: N={tokens}, E={edits}, D={deletions}, I={insertions}, S={substitutions}
           ''')
    print(f'''-----------------------------------
Sentence Error Rate:
Sum: N={num_sentences}, Err={num_sentences_error}
Avg: N={num_sentences}, Err={num_sentences_error/num_sentences*100:.2f}%
-----------------------------------
Word Error Rate:
Sum: N={num_words}, Err={num_errors}, Sub={num_substitutions}, Del={num_deletions}, Ins={num_insertions}
Avg: N={num_words}, Err={num_errors/num_words*100:.2f}%, Sub={num_substitutions/num_words*100:.2f}%, Del={num_deletions/num_words*100:.2f}%, Ins={num_insertions/num_words*100:.2f}%
-----------------------------------''')
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Evaluate ASR results.\n"
                                                 "Computes Word Error Rate and Sentence Error Rate")
    parser.add_argument(
        '-ht', '--hyptrn', help='Hypothesized transcripts in TRN format', required=True, default=None)
    parser.add_argument(
        '-rt', '--reftrn', help='Reference transcripts in TRN format', required=True, default=None)
    args = parser.parse_args()

    if args.reftrn is None or args.hyptrn is None:
        RuntimeError("Must specify reference trn and hypothesis trn files.")

    score(ref_trn=args.reftrn, hyp_trn=args.hyptrn)
