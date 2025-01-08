from langchain import PromptTemplate
from langchain.chains import ConversationChain, Chain
from transformers import AutoModelForCausalLM, AutoTokenizer

# Initialize the Hugging Face model and tokenizer
model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Define a custom chain for using DialoGPT with LangChain
class DialoGPTChain(Chain):
    def __init__(self, model, tokenizer):
        super().__init__()
        self.model = model
        self.tokenizer = tokenizer
    
    def _call(self, inputs):
        prompt = inputs['input']
        inputs_enc = self.tokenizer.encode(prompt + self.tokenizer.eos_token, return_tensors="pt")
        
        response = self.model.generate(
            inputs_enc,
            max_length=1000,
            pad_token_id=self.tokenizer.eos_token_id,
            temperature=0.7,
            top_k=50,
            top_p=0.9,
            no_repeat_ngram_size=2,
            early_stopping=True
        )
        
        decoded_response = self.tokenizer.decode(response[:, inputs_enc.shape[-1]:][0], skip_special_tokens=True)
        return {'output': decoded_response}

# Initialize LangChain with the custom chain
chat_chain = ConversationChain(
    chain=DialoGPTChain(model=model, tokenizer=tokenizer),
    prompt_template=PromptTemplate(template="User: {input}\nChatbot: ")
)

# Function to generate a response
def generate_response(prompt):
    result = chat_chain({"input": prompt})
    return result['output']
