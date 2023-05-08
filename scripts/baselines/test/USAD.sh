# USAD
export CUDA_VISIBLE_DEVICES=$1;
python test.py dataset=SWaT window_size=12 stride=12 eval_stride=12 batch_size=64 eval_batch_size=64 epochs=30 scaler=minmax model=USAD normalization=None model.latent_dim=40 infer_options=["offline_all"] +qStart=0.90 +qEnd=1.00 +qStep=0.01  &&
python test.py dataset=WADI window_size=12 stride=12 eval_stride=12 batch_size=64 eval_batch_size=64 epochs=30 scaler=minmax model=USAD scaler=minmax normalization=None  model.latent_dim=40 infer_options=["offline_all"] +qStart=0.90 +qEnd=1.00 +qStep=0.01  &&
python test.py dataset=PSM window_size=12 stride=12 eval_stride=12 batch_size=64 eval_batch_size=64 epochs=30 scaler=minmax model=USAD scaler=minmax normalization=None model.latent_dim=40 infer_options=["offline_all"] +qStart=0.90 +qEnd=1.00 +qStep=0.01  &&
python test.py dataset=CreditCard window_size=12 stride=12 eval_stride=12 batch_size=64 eval_batch_size=64 epochs=30 scaler=minmax model=USAD scaler=minmax normalization=None model.latent_dim=40 infer_options=["offline_all"] +qStart=0.90 +qEnd=1.00 +qStep=0.01  &&
python test.py dataset=MSL_P-15 window_size=5 stride=5 eval_stride=5 batch_size=8 eval_batch_size=8 epochs=30 scaler=minmax model=USAD scaler=minmax normalization=None model.latent_dim=33 infer_options=["offline_all"] +qStart=0.90 +qEnd=1.00 +qStep=0.01  &&
python test.py dataset=SMD_machine-1-4 window_size=5 stride=5 eval_stride=5 batch_size=8 eval_batch_size=8 epochs=30 scaler=minmax model=USAD scaler=minmax normalization=None model.latent_dim=38 infer_options=["offline_all"] +qStart=0.90 +qEnd=1.00 +qStep=0.01  &&
python test.py dataset=yahoo_20 window_size=5 stride=1 eval_stride=5 batch_size=8 eval_batch_size=8 epochs=30 scaler=minmax model=USAD scaler=minmax normalization=None model.latent_dim=40 infer_options=["offline_all"] +qStart=0.90 +qEnd=1.00 +qStep=0.01