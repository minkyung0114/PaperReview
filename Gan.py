import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
import os

(X_train, y_train), (_, _) = tf.keras.datasets.mnist.load_data()
X_train = X_train.reshape(X_train.shape[0], 28, 28, 1).astype('float32')
# X_train shape = (60000,28,28,1)
X_train = (X_train - 127.5) / 127.5
#범위가 -1에서 1 사이로 조절
buffer_size = 60000
batch_size = 256

X_train = tf.data.Dataset.from_tensor_slices(X_train).shuffle(buffer_size).batch(batch_size)
def build_generator():
    network = tf.keras.Sequential()
    network.add(layers.Dense(7*7*256,use_bias = False,input_shape=(100,)))
    network.add(layers.BatchNormalization())
    network.add(layers.LeakyReLU())
    network.add(layers.Reshape((7,7,256)))

    network.add(layers.Conv2DTranspose(128,(5,5),padding='same', use_bias=False))
    network.add(layers.BatchNormalization())
    network.add(layers.LeakyReLU())

    #14*14*64
    network.add(layers.Conv2DTranspose(64, (5, 5), strides=(2,2),padding='same', use_bias=False))
    network.add(layers.BatchNormalization())
    network.add(layers.LeakyReLU())

    # 28*28*1
    network.add(layers.Conv2DTranspose(1, (5, 5), strides=(2, 2), padding='same', use_bias=False, activation='tanh'))
    network.summary()

    return network



generator =  build_generator()
print(f"generator:{generator}")


noise = tf.random.normal([1,100])

generated_image = generator(noise,training=False)

plt.imshow(generated_image[0,:,:,0], cmap='gray')
#plt.show()

def build_discriminator():
    network = tf.keras.Sequential()

    #14*14*64
    network.add(layers.Conv2D(64,(5,5),strides=(2,2),padding='same', input_shape=[28,28,1]))
    network.add(layers.LeakyReLU())
    network.add(layers.Dropout(0.3))

    #7*7*128

    network.add(layers.Conv2D(128, (5, 5), strides=(2, 2), padding='same', input_shape=[28, 28, 1]))
    network.add(layers.LeakyReLU())
    network.add(layers.Dropout(0.3))

    network.add(layers.Flatten())

    network.add(layers.Dense(1))

    network.summary()

    return network

discriminator = build_discriminator()
#discriminator = dicreminator(generated_image,training=False)

cross_entropy = tf.keras.losses.BinaryCrossentropy(from_logits=True)

def discriminator_loss (expected_output, fake_output):
    real_loss = cross_entropy(tf.ones_like(expected_output), expected_output)
    fake_loss = cross_entropy(tf.zeros_like(fake_output), fake_output)
    total_loss = real_loss + fake_loss
    return total_loss

def generator_loss (fake_output):


    return cross_entropy(tf.ones_like(fake_output), fake_output)


generator_optimizer = tf.keras.optimizers.Adam(learning_rate=0.00001)
discriminator_optimizer = tf.keras.optimizers.Adam(learning_rate=0.00001)

noise_dim = 100
epochs =100
num_images_to_generate = 16
@tf.function
def train_steps(images):
    noise = tf.random.normal([batch_size,noise_dim])
    with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:

        generator_images = generator(noise,training=True)

        expected_output = discriminator(images,training=True)
        fake_output = discriminator(generator_images,training=True)

        gen_loss = generator_loss(fake_output)
        disc_loss = discriminator_loss(expected_output, fake_output)
        #print(f"gen_loss.:{gen_loss.numpy()},disc_loss:{disc_loss.numpy()}")
    gradients_of_generator = gen_tape.gradient(gen_loss, generator.trainable_variables)
    gradients_of_discriminator = disc_tape.gradient(disc_loss, discriminator.trainable_variables)

    generator_optimizer.apply_gradients(zip(gradients_of_generator,generator.trainable_variables))
    discriminator_optimizer.apply_gradients(zip(gradients_of_discriminator,discriminator.trainable_variables))


test_images = tf.random.normal([num_images_to_generate,noise_dim])
print(f"test image shape:{test_images.shape[0]}")

save_path = r"/PF/GAN"
os.makedirs(save_path,exist_ok=True)
save_path = save_path.replace("\\","/")
def train(dataset, epochs, test_images):
    for epoch in range(epochs):
        for image_batch in dataset:
            train_steps(image_batch)
        print(f"epoch:{epoch+1}")
        generated_images = generator(test_images,training=False)
        fig = plt.figure(figsize=(10,10))
        for i in range(generated_image.shape[0]):
            plt.subplot(4,4,i+1)
            plt.imshow(generated_images[i,:,:,0] *127.5+127.5, cmap='gray')
            plt.savefig(os.path.join(save_path,f"GAN_{epoch}.jpg"),dpi=300)
            plt.suptitle(f"GAN epoch : {epoch+1}")
            plt.axis('off')
        #plt.show()


if __name__ == "__main__":
    train(X_train,epochs,test_images)
