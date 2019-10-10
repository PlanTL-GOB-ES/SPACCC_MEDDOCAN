#!/usr/bin/python
import os
import argparse
from classes import i2b2Annotation, BratAnnotation, NER_Evaluation, Span_Evaluation
from collections import defaultdict

class evaluation(object):

    def __init__(self):
        self.format = None
        self.subtrack = []
        self.system = ""
        self.gs = ""
        self.format_name = ""
        self.subtask1 = ""
        self.subtask2 = ""

    def get_document_dict_by_system_id(self, system_dirs, annotation_format):
        """Takes a list of directories and returns annotations. """

        documents = defaultdict(lambda: defaultdict(int))

        for fn in os.listdir(system_dirs):
            if fn.endswith(".ann") or fn.endswith(".xml"):
                sa = annotation_format(os.path.join(system_dirs, fn))
                documents[sa.sys_id][sa.id] = sa

        return documents


    def subtracking(self,system_fo):
        for ta in os.listdir(system_fo):
            if ta.endswith("subtask1"):
                self.subtask1 = "subtask1"
                self.subtrack.append(NER_Evaluation)
            if ta.endswith("subtask2"):
                self.subtask2 = "subtask2"
                self.subtrack.append(Span_Evaluation)

    def setting(self, system):
            dir = os.path.join(system,"brat")
            if os.path.isdir(dir):
                self.format = BratAnnotation
                self.system = os.path.join(system, "brat")
                self.format_name = 'brat'
                self.subtracking(self.system)

            elif os.path.isdir(os.path.join(system,"xml")):
                self.format = i2b2Annotation
                self.system = os.path.join(system, "xml")
                self.format_name = 'xml'
                self.subtracking(self.system)
            else:
                Exception("Must pass brat or xml directory")

    def checking(self,gs):
        gs = os.path.join(gs, self.format_name)
        for st in self.subtrack:
            subtask = os.path.join(self.system, "subtask1" if st == NER_Evaluation else "subtask2")
            for filename in os.listdir(gs):
                if filename.endswith(".ann") or filename.endswith(".xml"):
                    result = os.path.isfile(os.path.join(subtask,filename))
                    if result == False:
                        return result

        return True


    def eval(self,input,output):
        """Evaluate the system by calling either NER_evaluation or Span_Evaluation.
        'system' can be a list containing either one file,  or one or more
        directories. 'gs' can be a file or a directory. """

        gold_ann = {}
        evaluations = []

        system = os.path.join(input,'res')
        gs = os.path.join(input, 'ref')


        # Handle the case where 'gs' is a directory and 'system' is a list of directories.
        if os.path.isdir(system) and os.path.isdir(gs):
            # Get a dict of gold annotations indexed by id


            self.setting(system)

            results  = []
            if not os.path.exists(output):
                os.makedirs(output)
            result_file = os.path.join(output,"scores.txt")
            file_W = open(result_file, 'w+')

            correctFile = self.checking(gs)

            if correctFile:
                gs = os.path.join(gs, self.format_name)
                for filename in os.listdir(gs):
                    if filename.endswith(".ann") or filename.endswith(".xml"):
                            annotations = self.format(os.path.join(gs, filename))
                            gold_ann[annotations.id] = annotations

                if len(self.subtrack) >=1:

                    for st in self.subtrack:
                        subtask = os.path.join(self.system,"subtask1" if st == NER_Evaluation else "subtask2")

                        for system_id, system_ann in sorted(self.get_document_dict_by_system_id(subtask, self.format).items()):
                            e = st(system_ann, gold_ann)
                            e.print_report(file_W)
                            evaluations.append(e)
                else:
                    print("You did not follow the submission structure\n")
                    file_W.write("You did not follow the submission structure\n")
                    file_W.write("Subtask1_Leak : {} \n".format("ERROR"))
                    file_W.write("Subtask1_Precision : {}\n".format("ERROR"))
                    file_W.write("Subtask1_Recall : {}\n".format("ERROR"))
                    file_W.write("Subtask1_F1 : {}\n".format("ERROR"))
                    file_W.write("Subtask2Strict_Precision : {}\n".format("ERROR"))
                    file_W.write("Subtask2Strict_Recall : {}\n".format("ERROR"))
                    file_W.write("Subtask2Strict_F1 : {}\n".format("ERROR"))
                    file_W.write("Subtask2Merged_Precision : {}\n".format("ERROR"))
                    file_W.write("Subtask2Merged_Recall : {}\n".format("ERROR"))
                    file_W.write("Subtask2Merged_F1 : {}\n".format("ERROR"))

            else:
                print("You did not annotate all data\n")
                file_W.write("You did not annotate all data\n")
                file_W.write("Subtask1_Leak : {} \n".format("ERROR"))
                file_W.write("Subtask1_Precision : {}\n".format("ERROR"))
                file_W.write("Subtask1_Recall : {}\n".format("ERROR"))
                file_W.write("Subtask1_F1 : {}\n".format("ERROR"))
                file_W.write("Subtask2Strict_Precision : {}\n".format("ERROR"))
                file_W.write("Subtask2Strict_Recall : {}\n".format("ERROR"))
                file_W.write("Subtask2Strict_F1 : {}\n".format("ERROR"))
                file_W.write("Subtask2Merged_Precision : {}\n".format("ERROR"))
                file_W.write("Subtask2Merged_Recall : {}\n".format("ERROR"))
                file_W.write("Subtask2Merged_F1 : {}\n".format("ERROR"))

            file_W.close()


        else:
            Exception("Must pass file file or [directory/]+ directory/"
                      "on command line!")

        return evaluations[0] if len(evaluations) == 1 else evaluations


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluation script for the MEDDOCAN track.")

    parser.add_argument("input_dir",
                        help="Directory to load GS and Submitions")
    parser.add_argument("output_dir",
                        help="Directory to print results")

    args = parser.parse_args()

    x = evaluation()
    x.eval(args.input_dir, args.output_dir)
