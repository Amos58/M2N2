#!/bin/bash
# LSTMEncDec
echo "gpu $1"
for SEED in 2021 2022 2023 2024 2025
do
#  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED save_roc_curve=True dataset=SWaT window_size=12 stride=12 eval_stride=12 batch_size=256 eval_batch_size=256 model=LSTMEncDec scaler=std normalization=None infer_options=["offline"] thresholding=off_f1_best  &&
#  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED save_roc_curve=True dataset=SWaT window_size=12 stride=12 eval_stride=12 batch_size=256 eval_batch_size=256 model=LSTMEncDec scaler=std normalization=None infer_options=["offline"] thresholding=q100  &&

#  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED save_roc_curve=True dataset=WADI window_size=12 stride=12 eval_stride=12 batch_size=256 eval_batch_size=256 model=LSTMEncDec scaler=std normalization=None infer_options=["offline"] thresholding=off_f1_best  &&
#
#  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED save_roc_curve=True dataset=SMD +dataset_id=machine-1-4 window_size=5 stride=5 eval_stride=5 batch_size=8 eval_batch_size=8 log_freq=1 model=LSTMEncDec scaler=std normalization=None infer_options=["offline"] thresholding=off_f1_best &&
#
#  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED save_roc_curve=True dataset=SMD +dataset_id=machine-2-1 window_size=5 stride=5 eval_stride=5 batch_size=8 eval_batch_size=8 log_freq=1 model=LSTMEncDec scaler=std normalization=None infer_options=["offline"] thresholding=off_f1_best &&
#  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED save_roc_curve=True dataset=SMD +dataset_id=machine-2-1 window_size=5 stride=5 eval_stride=5 batch_size=8 eval_batch_size=8 log_freq=1 model=LSTMEncDec scaler=std normalization=None infer_options=["offline"] thresholding=q100 &&
#
#  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED save_roc_curve=True dataset=MSL +dataset_id=P-15 window_size=5 stride=5 eval_stride=5 batch_size=8 eval_batch_size=8 log_freq=1 model=LSTMEncDec scaler=std normalization=None infer_options=["offline"] thresholding=off_f1_best  &&
#
#  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED save_roc_curve=True dataset=SMAP +dataset_id=T-3 window_size=5 stride=5 eval_stride=5 batch_size=8 eval_batch_size=8 log_freq=1 model=LSTMEncDec scaler=std normalization=None infer_options=["offline"] thresholding=off_f1_best  &&
#  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED save_roc_curve=True dataset=SMAP +dataset_id=T-3 window_size=5 stride=5 eval_stride=5 batch_size=8 eval_batch_size=8 log_freq=1 model=LSTMEncDec scaler=std normalization=None infer_options=["offline"] thresholding=q100  &&
#
#  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED save_roc_curve=True dataset=CreditCard window_size=12 stride=12 eval_stride=12 batch_size=256 eval_batch_size=256 model=LSTMEncDec scaler=std normalization=None infer_options=["offline"] thresholding=off_f1_best  &&
#
  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED save_roc_curve=True dataset=yahoo +dataset_id=real_20 window_size=5 stride=5 eval_stride=5 batch_size=8 eval_batch_size=8 log_freq=1 model=LSTMEncDec scaler=std normalization=None infer_options=["offline"] thresholding=off_f1_best &&
  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED save_roc_curve=True dataset=yahoo +dataset_id=real_20 window_size=5 stride=5 eval_stride=5 batch_size=8 eval_batch_size=8 log_freq=1 model=LSTMEncDec scaler=std normalization=None infer_options=["offline"] thresholding=q99 &&

  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED save_roc_curve=True dataset=yahoo +dataset_id=real_55 window_size=5 stride=5 eval_stride=5 batch_size=8 eval_batch_size=8 log_freq=1 model=LSTMEncDec scaler=std normalization=None infer_options=["offline"] thresholding=off_f1_best
done

