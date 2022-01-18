import torch
from django.conf import settings
from transformers import AutoTokenizer, AutoConfig, AutoModelForPreTraining

MODEL = 'gpt2'
SPECIAL_TOKENS = {
    'bos_token': '<|BOS|>',
    'eos_token': '<|EOS|>',
    'unk_token': '<|UNK|>',
    'pad_token': '<|PAD|>',
    'sep_token': '<|SEP|>'
}


def get_tokenizer(special_tokens=None):
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    tokenizer.add_special_tokens(special_tokens)
    return tokenizer


def get_model(tokenizer):
    config = AutoConfig.from_pretrained(
        MODEL,
        bos_token_id=tokenizer.bos_token_id,
        eos_token_id=tokenizer.eos_token_id,
        sep_token_id=tokenizer.sep_token_id,
        pad_token_id=tokenizer.pad_token_id,
        output_hidden_states=False
    )
    model = AutoModelForPreTraining.from_pretrained(MODEL, config=config)
    model.resize_token_embeddings(len(tokenizer))
    model.load_state_dict(torch.load(settings.GENERATOR_PRETRAINED_MODEL, map_location=torch.device('cpu')))
    return model


class Domain:
    tokenizer = get_tokenizer(SPECIAL_TOKENS)
    model = get_model(tokenizer)
    model.eval()

    @classmethod
    def generate_mail(cls, subject: str, summary: str):
        prompt = SPECIAL_TOKENS['bos_token'] + subject + \
                 SPECIAL_TOKENS['sep_token'] + summary + SPECIAL_TOKENS['sep_token']

        generated = torch.tensor(cls.tokenizer.encode(prompt)).unsqueeze(0)

        # beam-search text generation:
        sample_outputs = cls.model.generate(
            generated,
            do_sample=True,
            max_length=768,
            num_beams=5,
            repetition_penalty=5.0,
            early_stopping=True,
            num_return_sequences=1
        )
        text = cls.tokenizer.decode(sample_outputs[0], skip_special_tokens=True)
        a = len(subject) + len(summary)
        return text[a:]
