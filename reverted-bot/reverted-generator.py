import gpt_2_simple as gpt2
from datetime import datetime
import os

if not os.path.exists("./models/355M"):
    gpt2.download_gpt2(model_name="355M")

sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, run_name="run2")

gen_file = 'gpt2_gentext_{:%Y%m%d_%H%M%S}.txt'.format(datetime.utcnow())

"""
gpt2.generate_to_file(sess,
                      destination_path=gen_file,
                      length=200,
                      temperature=1.0,
                      top_p=0.9,
                      prefix='<|startoftext|>',
                      truncate='<|endoftext|>',
                      include_prefix=False,
                      nsamples=5,
                      batch_size=20,
                      run_name="run2"
                      )
"""
gpt2.generate(sess,
              run_name='run2',
              length=280,
              temperature=0.7,
              prefix="<|startoftext|>",
              truncate='<|endoftext|>',
              include_prefix=False,
              nsamples=1,
              batch_size=1)

