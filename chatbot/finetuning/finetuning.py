import os
import openai

os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = os.getenv("OPENAI_API_KEY")

training_file_name = 'C:/Users/dhapd/OneDrive/바탕 화면/chatbot/chatbot/finetuning/training.jsonl'
validation_file_name = 'C:/Users/dhapd/OneDrive/바탕 화면/chatbot/chatbot/finetuning/validation.jsonl'

training_response = openai.File.create(file=open(training_file_name, "rb"),purpose='fine-tune')
training_file_id = training_response["id"]

validation_response = openai.File.create(file=open(validation_file_name, "rb"),purpose='fine-tune')
validation_file_id = validation_response["id"]

print("Training file id:", training_file_id)
print("Validation file id:", validation_file_id)

suffix_name = "Chung-myung"

response = openai.FineTuningJob.create(
    training_file=training_file_id,
    validation_file=validation_file_id,
    model="gpt-3.5-turbo",
    suffix=suffix_name,
)

job_id = response["id"]

print(response)

response = openai.FineTuningJob.list_events(id=job_id, limit=50)

events = response["data"]
events.reverse()

for event in events:
    print(event["message"])

response = openai.FineTuningJob.retrieve(job_id)
fine_tuned_model_id = response["fine_tuned_model"]

print(response)
print("\nFine-tuned model id:", fine_tuned_model_id)