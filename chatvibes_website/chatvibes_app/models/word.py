import spacy
from django.db import models
from colorfield.fields import ColorField


from .validators import validate_word_name


spacy_model = spacy.load("en_core_web_trf")


class WordClassification(models.Model):
    name = models.CharField(primary_key=True, max_length=32, validators=[validate_word_name])
    description = models.TextField(default="", blank=True, max_length=1000)
    order_sequence = models.PositiveSmallIntegerField(
        default=100, help_text="Visual order of word classifications will be based on this.")
    color = ColorField(help_text="Visual color for this tag.")


class Word(models.Model):
    name = models.CharField(primary_key=True, max_length=32, validators=[validate_word_name])
    word_classification = models.ForeignKey(WordClassification, on_delete=models.RESTRICT)
    related_lemma_word = models.ForeignKey(
        "Word", editable=False, on_delete=models.RESTRICT,
        help_text="Related word that represents lemma word for this one.")
    is_lemma = models.BooleanField(
        default=False, editable=False,
        help_text="Does this word represent lemma of word, look up lemmatization.")

    def save(self, *args, **kwargs):
        """
        If record is being created we need to check if this word is lemma word,
        and if needed properly link it to one.
        """
        setup_needed = self._state.adding
        super().save(*args, **kwargs)
        if setup_needed:
            self._action_setup_word()

    def _action_setup_word(self):
        """Should be called for word setup, after the word is created for the first time."""
        # Check for is_lemma, if the word is lemma word then no further actions are needed.
        lemma_word = self.action_lemmatize_word(self.name)
        if lemma_word == self.name:
            self.is_lemma = True
            return

        # At this point the created word is not lemma word, link it to existing lemma word (and create if it's missing).
        existing_lemma_word = self.objects.filter(name=lemma_word)
        if not existing_lemma_word:
            existing_lemma_word = self.objects.create(
                name=lemma_word,
                word_classification=self.word_classification,
                is_lemma=True,
            )

        self.related_lemma_word = existing_lemma_word

    @classmethod
    def action_lemmatize_word(cls, word: str) -> str:
        """
        Costly model call.

        Lemmatization definition:
        To reduce the different forms of a word to one single form, for example,
        reducing "walking", "walks", or "walked" to the lemma "walk."""
        spacy_data = spacy_model(word)
        return spacy_data[0].lemma_
