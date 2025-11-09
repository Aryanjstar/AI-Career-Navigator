export enum RetrievalMode {
    Hybrid = "hybrid",
    Vectors = "vectors",
    Text = "text"
}

export enum VectorFields {
    TextAndImageEmbeddings = "text_and_image_embeddings",
    Text = "text",
    Image = "image"
}

export enum GPT4VInput {
    TextAndImages = "text_and_images",
    Text = "text",
    Images = "images"
}

export interface Approach {
    id: string;
    name: string;
    description: string;
}
