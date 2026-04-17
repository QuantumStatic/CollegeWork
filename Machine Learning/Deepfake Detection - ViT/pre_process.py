import pandas
from PIL import Image
import os
import pickle
from datasets import Dataset, load_dataset, dataset_dict, load_from_disk

from transformers import ViTFeatureExtractor
from sklearn.model_selection import train_test_split

if __name__ == "__main__":
    def main():

        # ds = load_from_disk('deepfake_dataset_ut/train')
        # ds = ds.train_test_split(test_size=0.2, shuffle=True)
        # print(type(ds))
        # print(ds['train'])

        # print(type(Image.open(r"data/manipulated/DF_745.png")))
        # df = pandas.read_csv("train.csv")
        
        model_path = 'google/vit-base-patch16-224-in21k'
        feature_extractor = ViTFeatureExtractor.from_pretrained(model_path)


        ## MAKING THE OG DATAFRAME

        # df = pandas.read_csv("labelled_data.csv")
        # new_df = df.rename(columns={"image_file_path":"pixel_values", "label":"labels"}, inplace=False)
        new_df = pandas.DataFrame(columns=["pixel_values", "labels"])
        *_, files = next(os.walk("data/manipulated"))

        for file in files:
            new_df = new_df.append({"pixel_values":f"data/manipulated/{file}", "labels":1}, ignore_index=True)

        *_, files = next(os.walk("data/original"))

        for file in files:
            new_df = new_df.append({"pixel_values":f"data/original/{file}", "labels":0}, ignore_index=True)
        
        # new_df = pandas.DataFrame(columns=["pixel_values", "labels"])

        
        # for _, row in df.iterrows():
            # print(row[0][1:])
            # break
            # new_df = new_df.append({'pixel_values': row[0][1:], 'labels': row[1]}, ignore_index=True)
            
        # new_df.to_csv("labelled_data2.csv", index=False)
        # new_df.to_pickle("labelled_data_fin.pkl")

        # print(new_df.loc[3])
        
        # ds = Dataset.from_pandas(new_df)
        # print("here", end="\n\n\n")
        # ds = ds.train_test_split(test_size=0.2, shuffle=True)
        # ds.save_to_disk("deepfake_dataset_ut")
        ## making the dataset dict
            # df = pandas.read_pickle("labelled_data_fin.pkl")

        train, test = train_test_split(new_df, test_size=0.2)
        train, validation = train_test_split(train, test_size=0.2)

        def convert_to_tensor(batch):
            batch["pixel_values"] = Image.open(batch["pixel_values"])
            return batch

        train_ds = Dataset.from_pandas(train)
        new_train_ds = train_ds.map(convert_to_tensor)
        new_train_ds.save_to_disk("deepfake_dataset_ut/train")

        test_ds = Dataset.from_pandas(test)
        new_test_ds = test_ds.map(convert_to_tensor)
        new_test_ds.save_to_disk("deepfake_dataset_ut/test")

        validation_ds = Dataset.from_pandas(validation)
        new_validation_ds = validation_ds.map(convert_to_tensor)
        new_validation_ds.save_to_disk("deepfake_dataset_ut/validation")

        fin = dataset_dict.DatasetDict({"train": new_train_ds, "test": new_test_ds, "validation": new_validation_ds})
        # fin.save_to_disk("deepfake_dataset_ut")

            # ds = dataset_dict = {"train":train_ds, "test":test_ds}
            # ds.save_to_disk("deepfake_dataset_ut")
    main()








