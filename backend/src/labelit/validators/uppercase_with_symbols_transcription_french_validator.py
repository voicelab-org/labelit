from django.core.exceptions import ValidationError


class UpperCaseWithSymbolsFrenchValidator:
    """
    Rules defined for this validator available at: https://docs.google.com/document/d/1NYq1GP_LM7kJ9ZTQOQbn-C5Iv-1WB0WLMN_x2KWTvBY
    """

    # Extracted from the list of characters used on CommonVoice 1
    VALID_CHARS = """\n !"$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_abcdefghijklmnopqrstuvwxyz{|}§«°º»½ÀÁÂÇÈÉÊÎÔàâçèéêëíîïñôöùûüÿŒœˢ–—’…₂€*"""

    UNACCEPTABLE_CHAR = "Unacceptable char!"
    WRONG_SYMBOL_TRANSCRIPTION_POURCENT = (
        "`Pourcent` word should be transcribed as `%`!"
    )
    WRONG_SYMBOL_TRANSCRIPTION_AROBASE = "`Arobase` word should be transcribed as `@`!"

    def validate(
        self,
        transcript,
    ):
        errors = []
        valid_chars_set = set(self.VALID_CHARS)
        for pos, c in enumerate(transcript):
            if (
                c not in valid_chars_set
            ):  # allowing new lines as well as valid characters
                errors.append(
                    f"{self.UNACCEPTABLE_CHAR} ({c}) at character index: {pos}"
                )

        for word in transcript.lower().split(" "):
            print(f"Word ***{word}****")
            if word == "arobase":
                errors.append(self.WRONG_SYMBOL_TRANSCRIPTION_AROBASE)

            if word == "pourcent":
                errors.append(self.WRONG_SYMBOL_TRANSCRIPTION_POURCENT)

        if len(errors):
            raise ValidationError("; ".join(errors))
