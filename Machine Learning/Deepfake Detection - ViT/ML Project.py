import torch
device = torch.device('mps' if torch.backends.mps.is_built() else 'cpu')
from datasets import Dataset, load_from_disk, dataset_dict, load_metric

import pandas
import numpy

from transformers import ViTForImageClassification, TrainingArguments, Trainer, ViTFeatureExtractor
from PIL import Image
import evaluate
from torchvision.transforms import ToTensor
from sklearn.model_selection import train_test_split

from myfunctions import execute_this

def collate_fn(batch):
    # print(*(batch[0]['pixel_values'].keys()))
    # input('>')
    return {
        'pixel_values': torch.stack([ToTensor()(Image.open(x['pixel_values'])).to(device) for x in batch]),
        'labels': torch.tensor([x['labels'] for x in batch]).to(device),
    }

metrics = load_metric("accuracy")
def compute_metrics(p):
    return metrics.compute(predictions=numpy.argmax(p.predictions, axis=1), references=p.label_ids)


if __name__ == "__main__":
    def main():

        # ds = Dataset.from_csv("labelled_data.csv")

        train_ds = load_from_disk("deepfake_dataset_ut/train")
        test_ds = load_from_disk("deepfake_dataset_ut/test")
        validation_ds = load_from_disk("deepfake_dataset_ut/validation")

        # print(validation_ds['pixel_values'])
        # return

        ds = dataset_dict.DatasetDict({"train":train_ds, "test":test_ds, "validation":validation_ds})

        model_path = "facebook/dino-vitb16"

        feature_extractor = ViTFeatureExtractor.from_pretrained(model_path)

        model = ViTForImageClassification.from_pretrained(
        model_path,
        num_labels=2,
        id2label={0:'0', 1:'1'},
        label2id={'0':0, '1':1}
        )

        model.to(device)

        training_args = TrainingArguments(
            output_dir="model_train/fb_vit",
            per_device_train_batch_size=18,
            evaluation_strategy="steps",
            num_train_epochs=4,
            fp16=False,
            save_steps=100,
            eval_steps=200,
            logging_steps=10,
            learning_rate=1e-5,
            save_total_limit=2,
            remove_unused_columns=False,
            push_to_hub=False,
            report_to='tensorboard',
            load_best_model_at_end=True,
            use_mps_device=True,
        )
        

        trainer = Trainer(
            model=model,
            args=training_args,
            data_collator=collate_fn,
            compute_metrics=compute_metrics,
            train_dataset=ds['train'],
            eval_dataset=ds['validation'],
            tokenizer=feature_extractor,
        )

        train_results = trainer.train()
        trainer.save_model()
        trainer.log_metrics("train", train_results.metrics)
        trainer.save_metrics("train", train_results.metrics)
        trainer.save_state()
        
        metrics = trainer.evaluate(ds['validation'])
        print(metrics)
        # trainer.log_metrics("eval", metrics)
        trainer.save_metrics("eval", metrics)
    main()
    

