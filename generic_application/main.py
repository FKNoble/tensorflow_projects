'''generic_application'''

# pylint: disable=E0401
# pylint: disable=C0103

# Import. Here, we import tensorflow, which gives us access to the library.
import os
import tensorflow as tf

if not os.path.exists('./data/output'):
    os.makedirs('./data/output')

if not os.path.exists('./model'):
    os.makedirs('./model')

if not os.path.exists('./logs'):
    os.makedirs('./logs')

# Here, we define helper functions for writing data to an example to a TFRecord file.
def float_feature(value):
    '''Create float_list-based feature'''
    return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))

def int_feature(value):
    '''Create float_list-based feature'''
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def bytes_feature(value):
    '''Create bytes_list-based feature'''
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

# Here, we define a function that makes an example, which is written to a TFRecord file.
def make_example(feature, label):
    '''Make example from feature'''

    example = tf.train.Example(features=tf.train.Features(feature={
        'feature': float_feature(feature),
        'label': float_feature(label),
    }))

    return example

# Here, we define a function that reads a TFRecord file; parsing a single example.
def read_record(filename_queue):
    '''Read record'''

    reader = tf.TFRecordReader()
    _, serialised_example = reader.read(filename_queue)

    example = tf.parse_single_example(
        serialised_example,
        features={
            'feature': tf.FixedLenFeature([], tf.float32),
            'label': tf.FixedLenFeature([], tf.float32),
        }
    )

    return example

def extract_example_data(example):
    '''Extract record'''

    feature = tf.cast(example['feature'], tf.float32)
    label = tf.cast(example['label'], tf.float32)

    return feature, label

# Here, we define a function that reads a TFRecord file.
def input_pipeline(filenames, num_epochs=1, batch_size=1):
    """Read a TFRecord"""

    filename_queue = tf.train.string_input_producer(
        filenames,
        num_epochs=num_epochs,
        shuffle=False
    )

    example = read_record(filename_queue)

    feature, label = extract_example_data(example)

    min_after_dequeue = 10000
    capacity = min_after_dequeue + 3 * batch_size
    feature_batch, label_batch = tf.train.batch(
        [feature, label],
        batch_size=batch_size,
        capacity=capacity,
        dynamic_pad=True)

    return feature_batch, label_batch

# Here, we define a function that writes a TFRecord file.
def output_pipeline(filenames, num_epochs=1):
    """Write a TFRecord"""

    filename_queue = tf.train.string_input_producer(
        filenames,
        num_epochs=num_epochs,
        shuffle=False
    )

    reader = tf.TextLineReader()
    _, value = reader.read(filename_queue)

    x, y = tf.decode_csv(value, record_defaults=[[0.0], [0.0]])

    return [x, y]

# Here, we define important directories.
input_dir = './data/input/'
output_dir = './data/output/'

# Here, we define important file names.
csv_file = input_dir + 'csv_data.csv'
record_file = output_dir + 'csv_record.tfrecords'

# Here, we define the number of times we read a record file, and what size each batch is.
num_epochs = 2
batch_size = 1

# Here, we create handles for reading and writing TFRecord files.
csv_data = output_pipeline([csv_file], 1)
record = input_pipeline([record_file], num_epochs, batch_size)

def MLP_layer(x, W, b):
    '''Default layer'''

    W = tf.get_variable(name='W', shape=W,
                        dtype=tf.float32, initializer=tf.constant_initializer(1.0))
    b = tf.get_variable(name='b', shape=b,
                        dtype=tf.float32, initializer=tf.constant_initializer(0.1))

    y_ = tf.add(tf.matmul(x, W), b)

    return y_

# Here, we define our graph: C = A + B.
with tf.name_scope('input'):
    A = tf.placeholder(tf.float32, shape=[None, 1], name='A')
    B = tf.placeholder(tf.float32, shape=[None, 1], name='B')

    # tf.summary.scalar('A', A)
    # tf.summary.scalar('B', B)

with tf.name_scope('output'):

    C = tf.Variable(0, name='C')

    C = A + B

    # tf.summary.scalar('C', C)

# Initialisation commands
init = [tf.global_variables_initializer(), tf.local_variables_initializer()]

# In this session, we read our raw data and create a TFRecord file.
with tf.Session() as s:

    s.run(init)

    writer = tf.python_io.TFRecordWriter(record_file)

    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=coord)

    try:
        while not coord.should_stop():

            feature, label = s.run(csv_data)

            example = make_example(feature, label)

            print(example)

            writer.write(example.SerializeToString())

    except tf.errors.OutOfRangeError:
        print('EoF')
    finally:
        coord.request_stop()

    coord.join(threads)

    writer.close()

# In this session, we read the TFRecord file and use its examples with our graph.
with tf.Session() as l:

    l.run(init)

    summary_writer = tf.summary.FileWriter('./logs', s.graph)

    merged = tf.summary.merge_all()

    saver = tf.train.Saver()
    saver.save(l, './model/main.ckpt', 0)
    saver.export_meta_graph('./model/main.meta')

    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=coord)

    try:
        i = 0

        while not coord.should_stop():

            x, y = l.run(record)

            x = l.run(tf.reshape(x, [batch_size, 1]))
            y = l.run(tf.reshape(y, [batch_size, 1]))

            feed_dict = {A: x, B: y}
            summary, ans = l.run([merged, C], feed_dict)

            summary_writer.add_summary(summary, i)

            print(ans)

            if i%5 == 0:
                saver.save(l, './model/main.ckpt', i)

            i += 1

    except tf.errors.OutOfRangeError:
        print('EoF')
    finally:
        coord.request_stop()

    coord.join(threads)

# Here, we restore our latest checkpoint and test our graph.
with tf.Session() as f:

    f.run(init)

    loader = tf.train.import_meta_graph('./model/main.meta')
    ckpt = tf.train.latest_checkpoint('./model/')
    loader.restore(f, ckpt)

    ans = f.run(C, {A: [[2.0]], B: [[5.0]]})

    print(ans)
