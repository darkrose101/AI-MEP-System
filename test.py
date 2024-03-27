from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
# Load the pre-trained model and tokenizer
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Function to generate a summary for a given review
def generate_summary(review):
    # Tokenize the review
    inputs = tokenizer.encode(review, return_tensors="pt")
    
    # Generate the summary
    summary_ids = model.generate(inputs, max_length=50, num_return_sequences=1)
    
    # Decode the summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
    return summary

# Test the function
print(generate_summary("great"))
print(generate_summary("disappointing"))
print(generate_summary("good"))