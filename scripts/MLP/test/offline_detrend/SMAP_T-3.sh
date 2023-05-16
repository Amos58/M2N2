export CUDA_VISIBLE_DEVICES=$1;
python test.py dataset=SMAP_T-3 window_size=5 stride=5 eval_stride=5 batch_size=8 log_freq=1 normalization=Detrend model=MLP model.latent_dim=16 \
 gamma=0.8 \
 infer_options=["offline_detrend_all"] +qStart=0.90 +qEnd=1.00 +qStep=0.01