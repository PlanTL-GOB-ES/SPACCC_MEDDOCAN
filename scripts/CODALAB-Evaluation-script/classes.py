import os
from tags import PHITag
from xml.etree import ElementTree


class Annotation(object):

    def __init__(self, file_name=None, root="root"):
        self.doc_id = ''
        self.sys_id = ''
        self.text = None
        self.num_sentences = None
        self.root = root
        self.sensitive_spans = []
        self.sensitive_spans_merged = []
        self.verbose = False

        if file_name:
            self.sys_id = os.path.basename(os.path.dirname(file_name))
            self.doc_id = os.path.splitext(os.path.basename(file_name))[0]
        else:
            self.doc_id = None

    @property
    def id(self):
        return self.doc_id

    def get_phi(self):
        return self.phi

    def get_phi_spans(self):
        return self.sensitive_spans

    def get_phi_spans_merged(self):
        return self.sensitive_spans_merged

    def get_phi_spans_joins(self):
        return self.sensitive_spans_joins

    def get_number_sentences(self):
        import os
        try:
            self.num_sentences = \
                sum(1 for line in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'annotated_corpora/sentence_splitted/') +
                                       self.doc_id +
                                       ".ann"))
        except IOError:
            print("File '" +
                  'freeling/sentence_splitted/' +
                  self.doc_id +
                  ".ann' not found.")
        return self.num_sentences

    def add_spans(self, phi_tags):
        for tag in sorted(phi_tags):
            self.sensitive_spans.append(tag)

        for y in sorted(phi_tags):
            if not self.sensitive_spans_merged:
                self.sensitive_spans_merged.append(y)
            else:
                x = self.sensitive_spans_merged.pop()
                if self.is_all_non_alphanumeric(self.text[x[1]:y[0]]):
                    self.sensitive_spans_merged.append((x[0], y[1]))
                else:
                    self.sensitive_spans_merged.append(x)
                    self.sensitive_spans_merged.append(y)

    @staticmethod
    def is_all_non_alphanumeric(string):
        for i in string:
            if i.isalnum():
                return False
        return True


class i2b2Annotation(Annotation):
    """ This class models the i2b2 annotation format."""

    def __init__(self, file_name=None, root="root"):
        self.doc_id = ''
        self.sys_id = ''
        self.text = None
        self.num_sentences = None
        self.root = root
        self.phi = []
        self.sensitive_spans = []
        self.sensitive_spans_merged = []
        self.verbose = False

        if file_name:
            self.sys_id = os.path.basename(os.path.dirname(file_name))
            self.doc_id = os.path.splitext(os.path.basename(file_name))[0]

            self.parse_text_and_tags(file_name)
            self.parse_text_and_spans(file_name)
            self.file_name = file_name
        else:
            self.doc_id = None

    def parse_text_and_tags(self, file_name=None):
        if file_name is not None:
            text = open(file_name, 'r').read()
            self.text = text

            tree = ElementTree.parse(file_name)
            root = tree.getroot()

            self.root = root.tag

            try:
                self.text = root.find("TEXT").text
            except AttributeError:
                self.text = None

            # Handles files where PHI, and AnnotatorTags are all just
            # stuffed into tag element.
            for t, cls in PHITag.tag_types.items():
                if len(root.find("TAGS").findall(t)):
                    for element in root.find("TAGS").findall(t):
                        self.phi.append(cls(element))

    def parse_text_and_spans(self, file_name=None):

        if file_name is not None:
            text = open(file_name, 'r').read()
            self.text = text

            tree = ElementTree.parse(file_name)
            root = tree.getroot()

            self.root = root.tag

            try:
                self.text = root.find("TEXT").text
            except AttributeError:
                self.text = None

            # Fill list with tuples (start, end) for each annotation
            phi_tags = []
            for t, cls in PHITag.tag_types.items():
                if len(root.find("TAGS").findall(t)):
                    for element in root.find("TAGS").findall(t):
                        phi_tags.append((cls(element).get_start(), cls(element).get_end()))

            # Store spans
            self.add_spans(phi_tags)


class BratAnnotation(Annotation):
    """ This class models the BRAT annotation format."""

    def __init__(self, file_name=None, root="root"):
        self.doc_id = ''
        self.sys_id = ''
        self.text = None
        self.num_sentences = None
        self.root = root
        self.phi = []
        self.sensitive_spans = []
        self.sensitive_spans_merged = []
        self.verbose = False

        if file_name:
            self.sys_id = os.path.basename(os.path.dirname(file_name))
            self.doc_id = os.path.splitext(os.path.basename(file_name))[0]

            self.parse_text_and_tags(file_name)
            self.parse_text_and_spans(file_name)
            self.file_name = file_name
        else:
            self.doc_id = None

    def parse_text_and_tags(self, file_name=None):
        if file_name is not None:
            text = open(os.path.splitext(file_name)[0] + '.txt', 'r').read()
            self.text = text

            for row in open(file_name, 'r'):
                line = row.strip()
                if line.startswith("T"):  # Lines is a Brat TAG
                    try:
                        label = line.split("\t")[1].split()
                        tag = label[0]
                        start = int(label[1])
                        end = int(label[2])
                        self.phi.append((tag, start, end))
                    except IndexError:
                        print("ERROR! Index error while splitting sentence '" +
                              line + "' in document '" + file_name + "'!")
                else:  # Line is a Brat comment
                    if self.verbose:
                        print("\tSkipping line (comment):\t" + line)

    def parse_text_and_spans(self, file_name=None):

        if file_name is not None:
            text = open(os.path.splitext(file_name)[0] + '.txt', 'r').read()
            self.text = text

            phi_tags = []
            for row in open(file_name, 'r'):
                line = row.strip()
                if line.startswith("T"):  # Lines is a Brat TAG
                    try:
                        label = line.split("\t")[1].split()
                        start = int(label[1])
                        end = int(label[2])

                        phi_tags.append((start, end))
                    except IndexError:
                        print("ERROR! Index error while splitting sentence '" +
                              line + "' in document '" + file_name + "'!")
                else:  # Line is a Brat comment
                    if self.verbose:
                        print("\tSkipping line (comment):\t" + line)

            # Store spans
            self.add_spans(phi_tags)


class Evaluate(object):
    """Base class with all methods to evaluate the different subtracks."""

    def __init__(self, sys_ann, gs_ann):
        self.tp = []
        self.fp = []
        self.fn = []
        self.doc_ids = []
        self.verbose = False

        self.sys_id = sys_ann[list(sys_ann.keys())[0]].sys_id

    @staticmethod
    def get_tagset_ner(annotation):
        return annotation.get_phi()

    @staticmethod
    def get_tagset_span(annotation):
        return annotation.get_phi_spans()

    @staticmethod
    def get_tagset_span_merged(annotation):
        return annotation.get_phi_spans_merged()

    @staticmethod
    def is_contained(content, container):
        for element in sorted(container):
            if content[0] >= element[0] and content[1] <= element[1]:
                return True
        return False

    @staticmethod
    def recall(tp, fn):
        try:
            return len(tp) / float(len(fn) + len(tp))
        except ZeroDivisionError:
            return 0.0

    @staticmethod
    def precision(tp, fp):
        try:
            return len(tp) / float(len(fp) + len(tp))
        except ZeroDivisionError:
            return 0.0

    @staticmethod
    def F_beta(p, r, beta=1):
        try:
            return (1 + beta**2) * ((p * r) / (p + r))
        except ZeroDivisionError:
            return 0.0

    def micro_recall(self):
        try:
            return sum([len(t) for t in self.tp]) /  \
                float(sum([len(t) for t in self.tp]) +
                      sum([len(t) for t in self.fn]))
        except ZeroDivisionError:
            return 0.0

    def micro_precision(self):
        try:
            return sum([len(t) for t in self.tp]) /  \
                float(sum([len(t) for t in self.tp]) +
                      sum([len(t) for t in self.fp]))
        except ZeroDivisionError:
            return 0.0

    def _print_docs(self):
        for i, doc_id in enumerate(self.doc_ids):
            mp = Evaluate.precision(self.tp[i], self.fp[i])
            mr = Evaluate.recall(self.tp[i], self.fn[i])

            str_fmt = "{:<35}{:<15}{:<20}"

            print(str_fmt.format(doc_id,
                                 "Precision",
                                 "{:.4}".format(mp)))

            print(str_fmt.format("",
                                 "Recall",
                                 "{:.4}".format(mr)))

            print(str_fmt.format("",
                                 "F1",
                                 "{:.4}".format(Evaluate.F_beta(mp, mr))))

            print("{:-<60}".format(""))

    def _print_summary(self, file_W):
        mp = self.micro_precision()
        mr = self.micro_recall()

        if self.label == "SubTrack 2 [strict]":
            file_W.write("Subtask2Strict_Precision : {}\n".format(mp))
            file_W.write("Subtask2Strict_Recall : {}\n".format(mr))
            file_W.write("Subtask2Strict_F1 : {}\n".format(Evaluate.F_beta(mr, mp)))

            print("Subtask2Strict_Precision : {}\n".format(mp))
            print("Subtask2Strict_Recall : {}\n".format(mr))
            print("Subtask2Strict_F1 : {}\n".format(Evaluate.F_beta(mr, mp)))
        elif self.label == "SubTrack 2 [merged]":
            file_W.write("Subtask2Merged_Precision : {}\n".format(mp))
            file_W.write("Subtask2Merged_Recall : {}\n".format(mr))
            file_W.write("Subtask2Merged_F1 : {}\n".format(Evaluate.F_beta(mr, mp)))

            print("Subtask2Merged_Precision : {}\n".format(mp))
            print("Subtask2Merged_Recall : {}\n".format(mr))
            print("Subtask2Merged_F1 : {}\n".format(Evaluate.F_beta(mr, mp)))


    def print_docs(self):
        print("\n")
        print("Report ({}):".format(self.sys_id))
        print("{:-<60}".format(""))
        print("{:<35}{:<15}{:<20}".format("Document ID", "Measure", "Micro"))
        print("{:-<60}".format(""))
        self._print_docs()

    def print_report(self, file_W):
        self._print_summary(file_W)


class EvaluateSubtrack1(Evaluate):
    """Class for running the NER evaluation."""

    def __init__(self, sys_sas, gs_sas):
        self.tp = []
        self.fp = []
        self.fn = []
        self.num_sentences = []
        self.doc_ids = []
        self.verbose = False

        self.sys_id = sys_sas[list(sys_sas.keys())[0]].sys_id
        self.label = "Subtrack 1 [NER]"

        for doc_id in sorted(list(set(sys_sas.keys()) & set(gs_sas.keys()))):
            gold = set(self.get_tagset_ner(gs_sas[doc_id]))
            sys = set(self.get_tagset_ner(sys_sas[doc_id]))
            num_sentences = self.get_num_sentences(sys_sas[doc_id])

            self.tp.append(gold.intersection(sys))
            self.fp.append(sys - gold)
            self.fn.append(gold - sys)
            self.num_sentences.append(num_sentences)
            self.doc_ids.append(doc_id)

    @staticmethod
    def get_num_sentences(annotation):
        return annotation.get_number_sentences()

    @staticmethod
    def leak_score(fn, num_sentences):
        try:
            return float(len(fn) / num_sentences)
        except ZeroDivisionError:
            return 0.0
        except TypeError:
            return "NA"

    def micro_leak(self):
        try:
            return float(sum([len(t) for t in self.fn]) / sum(t for t in self.num_sentences))
        except ZeroDivisionError:
            return 0.0
        except TypeError as error:
            print(error)
            return 'NA'

    def _print_docs(self):
        for i, doc_id in enumerate(self.doc_ids):
            mp = EvaluateSubtrack1.precision(self.tp[i], self.fp[i])
            mr = EvaluateSubtrack1.recall(self.tp[i], self.fn[i])
            leak = EvaluateSubtrack1.leak_score(self.fn[i], self.num_sentences[i])

            str_fmt = "{:<35}{:<15}{:<20}"

            print(str_fmt.format(doc_id,
                                 "Leak",
                                 "{:.4}".format(leak)))

            print(str_fmt.format("",
                                 "Precision",
                                 "{:.4}".format(mp)))

            print(str_fmt.format("",
                                 "Recall",
                                 "{:.4}".format(mr)))

            print(str_fmt.format("",
                                 "F1",
                                 "{:.4}".format(Evaluate.F_beta(mp, mr))))

            print("{:-<60}".format(""))

    def _print_summary(self, file_W):
        mp = self.micro_precision()
        mr = self.micro_recall()
        ml = self.micro_leak()


        file_W.write("Subtask1_Leak : {} \n".format(ml))
        file_W.write("Subtask1_Precision : {}\n".format(mp))
        file_W.write("Subtask1_Recall : {}\n".format(mr))
        file_W.write("Subtask1_F1 : {}\n".format(Evaluate.F_beta(mr, mp)))

        print("Subtask1_Leak : {}\n".format(ml))
        print("Subtask1_Precision : {}\n".format(mp))
        print("Subtask1_Recall : {}\n".format(mr))
        print("Subtask1_F1 : {}\n".format(Evaluate.F_beta(mr, mp)))


class EvaluateSubtrack2(Evaluate):
    """Class for running the SPAN evaluation with strict span mode."""

    def __init__(self, sys_sas, gs_sas):
        self.tp = []
        self.fp = []
        self.fn = []
        self.doc_ids = []
        self.verbose = False

        self.sys_id = sys_sas[list(sys_sas.keys())[0]].sys_id
        self.label = "Subtrack 2 [strict]"

        for doc_id in sorted(list(set(sys_sas.keys()) & set(gs_sas.keys()))):

            gold = set(self.get_tagset_span(gs_sas[doc_id]))
            sys = set(self.get_tagset_span(sys_sas[doc_id]))

            self.tp.append(gold.intersection(sys))
            self.fp.append(sys - gold)
            self.fn.append(gold - sys)
            self.doc_ids.append(doc_id)


class EvaluateSubtrack2merged(Evaluate):
    """Class for running the SPAN evaluation with merged spans mode."""

    def __init__(self, sys_sas, gs_sas):
        self.tp = []
        self.fp = []
        self.fn = []
        self.doc_ids = []
        self.verbose = False

        self.sys_id = sys_sas[list(sys_sas.keys())[0]].sys_id
        self.label = "Subtrack 2 [merged]"

        for doc_id in sorted(list(set(sys_sas.keys()) & set(gs_sas.keys()))):

            gold_strict = set(self.get_tagset_span(gs_sas[doc_id]))
            sys_strict = set(self.get_tagset_span(sys_sas[doc_id]))

            gold_merged = set(self.get_tagset_span_merged(gs_sas[doc_id]))
            sys_merged = set(self.get_tagset_span_merged(sys_sas[doc_id]))

            intersection = gold_strict.intersection(sys_strict).union(gold_merged.intersection(sys_merged))

            fp = sys_strict - gold_strict
            for tag in sys_strict:
                if self.is_contained(tag, intersection):
                    if tag in fp:
                        fp.remove(tag)

            fn = gold_strict - sys_strict
            for tag in gold_strict:
                if self.is_contained(tag, intersection):
                    if tag in fn:
                        fn.remove(tag)

            self.tp.append(intersection)
            self.fp.append(fp)
            self.fn.append(fn)
            self.doc_ids.append(doc_id)


class MeddocanEvaluation(object):
    """Base class for running the evaluations."""

    def __init__(self):
        self.evaluations = []

    def add_eval(self, e, label=""):
        e.sys_id = "SYSTEM: " + e.sys_id
        e.label = label
        self.evaluations.append(e)

    def print_docs(self):
        for e in self.evaluations:
            e.print_docs()

    def print_report(self, file_W=None):
        for e in self.evaluations:
            e.print_report(file_W)


class NER_Evaluation(MeddocanEvaluation):
    """Class for running the NER evaluation (Subtrack 1)."""

    def __init__(self, annotator_cas, gold_cas, **kwargs):
        self.evaluations = []

        # Basic Evaluation
        self.add_eval(EvaluateSubtrack1(annotator_cas, gold_cas, **kwargs),
                      label="SubTrack 1 [NER]")


class Span_Evaluation(MeddocanEvaluation):
    """Class for running the SPAN evaluation (Subtrack 2). Calls to 'strict'
    and 'merged' evaluations. """

    def __init__(self, annotator_cas, gold_cas, **kwargs):
        self.evaluations = []

        self.add_eval(EvaluateSubtrack2(annotator_cas, gold_cas, **kwargs),
                      label="SubTrack 2 [strict]")

        self.add_eval(EvaluateSubtrack2merged(annotator_cas, gold_cas, **kwargs),
                      label="SubTrack 2 [merged]")
