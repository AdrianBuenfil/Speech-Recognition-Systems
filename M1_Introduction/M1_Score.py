import argparse
import wer
import re

# create a function that calls wer.string_edit_distance() on every utterance
# and accumulates the errors for the corpus. Then, report the word error rate (WER)
# and the sentence error rate (SER). The WER should include the the total errors as well as the
# separately reporting the percentage of insertions, deletions and substitutions.
# The function signature is
# num_tokens, num_errors, num_deletions, num_insertions, num_substitutions = wer.string_edit_distance(
# ref=reference_string, hyp=hypothesis_string)


def score(ref_trn=None, hyp_trn=None):
    reference_string = ""
    hypothesis_string = ""
    num_sentences = 0
    with open(ref_trn) as reference, open(hyp_trn) as hypothesis:
        for lineR, lineH in zip(reference, hypothesis):

            id_ref_pattern = re.compile(r'\(.+\)')
            id_ref_match = id_ref_pattern.search(lineR)
            reference_string = lineR[:id_ref_match.start()]

            id_hyp_pattern = re.compile(r'\(.+\)')
            id_hyp_match = id_hyp_pattern.search(lineH)
            hypothesis_string = lineH[:id_hyp_match.start()]
                       
            # count how many words are there

            print(reference_string + id_ref_match[0])
            print(hypothesis_string + id_hyp_match[0])
            tokens, edits, deletions, insertions, substitutions = wer.string_edit_distance(
        ref=reference_string, hyp=hypothesis_string)
            print(tokens, edits, deletions, insertions, substitutions)
            num_sentences += 1
    print(num_sentences)
    return


if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Evaluate ASR results.\n"
                                                 "Computes Word Error Rate and Sentence Error Rate")
    parser.add_argument('-ht', '--hyptrn', help='Hypothesized transcripts in TRN format', required=True, default=None)
    parser.add_argument('-rt', '--reftrn', help='Reference transcripts in TRN format', required=True, default=None)
    args = parser.parse_args()

    if args.reftrn is None or args.hyptrn is None:
        RuntimeError("Must specify reference trn and hypothesis trn files.")

    score(ref_trn=args.reftrn, hyp_trn=args.hyptrn)

#score(ref_trn="ref.trn", hyp_trn="hyp.trn")

# Total number of reference sentences in the test set N=3
# Number of sentences with an error Err=3
# Sentence error rate as a percentage SER = Err/N as %
# Total number of reference words M = additive word count for reference string
# Total number of word errors Err = Sub + Del + Ins
# Total number of word substitutions, insertions, and deletions Sub, Del, Ins
# The percentage of total errors (WER) and percentage of substitutions, 
#           insertions, and deletions WER = Err/M, Sub/M, Del/M, Ins/M

# id: (0000-000000-0000)
# Scores: N=6, S=0, D=1, I=1

# id: (0000-000000-0001)
# Scores: N=6, S=2, D=0, I=0

# id: (0000-00000-0002)
# Scores: N=6, S=2, D=1, I=1

# -----------------------------------
# Sentence Error Rate:
# Sum: N=3, Err=3
# Avg: N=3, Err=100.00%
# -----------------------------------
# Word Error Rate:
# Sum: N=18, Err=8, Sub=4, Del=2, Ins=2
# Avg: N=18, Err=44.44%, Sub=22.22%, Del=11.11%, Ins=11.11%
# -----------------------------------