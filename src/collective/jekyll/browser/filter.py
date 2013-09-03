from itertools import islice, count

from collective.jekyll.interfaces import IDiagnosis


class DiagnosisFilter(object):

    def __init__(self, seq, length, symptom_name=None):
        self._seq = seq
        self._invalid = []
        self._valid = []
        self._end_index = -1
        self._len = length
        self.symptom_name = symptom_name

    def __getitem__(self, index):
        invalid = self._invalid
        invalid_len = len(invalid)
        valid = self._valid
        valid_len = len(valid)
        try:
            s = self._seq
        except AttributeError:
            if index < 0:
                index = index + self._len
            if index < invalid_len:
                return invalid[index]
            else:
                return valid[index - invalid_len]

        i = index
        if i < 0:
            i = len(self) + i
        if i < 0:
            raise IndexError(index)
        if i > self._len:
            raise IndexError(index)

        if i < invalid_len:
            return invalid[i]
        invalid_len = invalid_len - 1

        e = self._end_index
        while i > invalid_len:
            try:
                e = e + 1
                v = s[e]
                diagnosis = IDiagnosis(v)
                if self.getItemStatus(diagnosis):
                    valid.append((v, diagnosis))
                    valid_len += 1
                else:
                    invalid.append((v, diagnosis))
                    invalid_len += 1
            except IndexError:
                del self._seq
                break
        self._end_index = e
        if i == invalid_len:
            return invalid[i]
        else:
            return valid[i - invalid_len - 1]

    def getItemStatus(self, diagnosis):
        if self.symptom_name is None:
            return diagnosis.status
        else:
            return diagnosis.getStatusByName(self.symptom_name)

    def __len__(self):
        return self._len

    def __getslice__(self, i1, i2):
        r = []
        for i in islice(count(i1), i2 - i1):
            try:
                r.append(self[i])
            except IndexError:
                return r
        return r

    slice = __getslice__
