from django.core.exceptions import ValidationError


class BaseRealtimeDimensionalAnnotationValidator:
    def validate(self, label):
        pass
        """
        errors = []
        valid_chars_set = set(self.valid_chars)
        for pos, c in enumerate(transcript):
            if (
                c not in valid_chars_set and not c == "\n"
            ):  # allowing new lines as well as valid characters
                errors.append((pos, self.case1_error))
                break
        if len(errors):
            raise ValidationError(
                "; ".join([e[1] + " at character index: " + str(e[0]) for e in errors])
            )
        """
