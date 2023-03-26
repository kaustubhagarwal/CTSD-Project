Import os
import csv
import tensorflow as tf
import tokenization


class InputExample(object):

  def __init__(self, guid, text_a, text_b=None, label=None):
    self.guid = guid
    self.text_a = text_a
    self.text_b = text_b
    self.label = label


class PaddingInputExample(object):


class InputFeatures(object):

  def __init__(self,
               input_ids,
               input_mask,
               segment_ids,
               label_id,
               label_mask=None,
               is_real_example=True):
    self.input_ids = input_ids
    self.input_mask = input_mask
    self.segment_ids = segment_ids
    self.label_id = label_id
    self.is_real_example = is_real_example
    self.label_mask = label_mask


class DataProcessor(object):

  def get_labeled_examples(self, data_dir):
    raise NotImplementedError()

  def get_unlabeled_examples(self, data_dir):
    raise NotImplementedError()

  def get_test_examples(self, data_dir):
    raise NotImplementedError()

  def get_labels(self):
    raise NotImplementedError()

  @classmethod
  def _read_tsv(cls, input_file, quotechar=None):
    with tf.gfile.Open(input_file, "r") as f:
      reader = csv.reader(f, delimiter="\t", quotechar=quotechar)
      lines = []
      for line in reader:
        lines.append(line)
      return lines

class QcFineProcessor(DataProcessor):

    def get_labeled_examples(self, data_dir):
        return self._create_examples(os.path.join(data_dir, "labeled.tsv"), "train")

    def get_unlabeled_examples(self, data_dir):
        return self._create_examples(os.path.join(data_dir, "unlabeled.tsv"), "train")

    def get_test_examples(self, data_dir):
        return self._create_examples(os.path.join(data_dir, "test.tsv"), "test")

    def get_labels(self):
        return ["UNK_UNK", "ABBR_abb", "ABBR_exp", "DESC_def", "DESC_desc", "DESC_manner", "DESC_reason", "ENTY_animal", "ENTY_body", "ENTY_color", "ENTY_cremat", "ENTY_currency", "ENTY_dismed", "ENTY_event", "ENTY_food", "ENTY_instru", "ENTY_lang", "ENTY_letter", "ENTY_other", "ENTY_plant", "ENTY_product", "ENTY_religion", "ENTY_sport", "ENTY_substance", "ENTY_symbol", "ENTY_techmeth", "ENTY_termeq", "ENTY_veh", "ENTY_word", "HUM_desc", "HUM_gr", "HUM_ind", "HUM_title", "LOC_city", "LOC_country", "LOC_mount", "LOC_other", "LOC_state", "NUM_code", "NUM_count", "NUM_date", "NUM_dist", "NUM_money", "NUM_ord", "NUM_other", "NUM_perc", "NUM_period", "NUM_speed", "NUM_temp", "NUM_volsize", "NUM_weight"]

    def _create_examples(self, input_file, set_type):
        examples = []

        with open(input_file, 'r') as f:
            contents = f.read()
            file_as_list = contents.splitlines()
            for line in file_as_list[1:]:
                split = line.split(" ")
                question = ' '.join(split[1:])

                guid = "%s-%s" % (set_type, tokenization.convert_to_unicode(line))
                text_a = tokenization.convert_to_unicode(question)
                inn_split = split[0].split(":")
                label = inn_split[0] + "_" + inn_split[1]
                examples.append(InputExample(guid=guid, text_a=text_a, text_b=None, label=label))
            f.close()

        return examples
