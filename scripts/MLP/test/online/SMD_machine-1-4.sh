export CUDA_VISIBLE_DEVICES=$1;
python test.py dataset=SMD_machine-1-4 window_size=5 stride=5 eval_stride=5 batch_size=8 log_freq=1 normalization=None model=MLP model.latent_dim=16 \
 ttlr=0.1 \
 infer_options=["online_all"] +qStart=0.90 +qEnd=1.00 +qStep=0.01