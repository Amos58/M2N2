#!/bin/bash
# AnomalyTransformer
echo "gpu $1"
#for SEED in 2021 2022 2023 2024 2025
for SEED in 2023
do
  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED dataset=SWaT save_roc_curve=True window_size=100 stride=100 eval_stride=100 batch_size=256 eval_batch_size=256 normalization=None model=AnomalyTransformer model.anomaly_ratio=0.5 infer_options=["offline"] thresholding=off_f1_best &&
  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED dataset=SWaT save_roc_curve=True window_size=100 stride=100 eval_stride=100 batch_size=256 eval_batch_size=256 normalization=None model=AnomalyTransformer model.anomaly_ratio=0.5 infer_options=["offline"] thresholding=q99 &&

  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED dataset=WADI save_roc_curve=True window_size=100 stride=100 eval_stride=100 batch_size=256 eval_batch_size=256 normalization=None model=AnomalyTransformer model.anomaly_ratio=0.5  infer_options=["offline"] thresholding=off_f1_best &&
  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED dataset=WADI save_roc_curve=True window_size=100 stride=100 eval_stride=100 batch_size=256 eval_batch_size=256 normalization=None model=AnomalyTransformer model.anomaly_ratio=0.5  infer_options=["offline"] thresholding=q99

  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED dataset=SMD +dataset_id=machine-1-4 save_roc_curve=True window_size=100 stride=100 eval_stride=100 batch_size=1 eval_batch_size=1 normalization=None model=AnomalyTransformer model.anomaly_ratio=0.5 infer_options=["offline"] thresholding=off_f1_best &&
  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED dataset=SMD +dataset_id=machine-1-4 save_roc_curve=True window_size=100 stride=100 eval_stride=100 batch_size=1 eval_batch_size=1 normalization=None model=AnomalyTransformer model.anomaly_ratio=0.5 infer_options=["offline"] thresholding=q99 &&

  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED dataset=SMD +dataset_id=machine-2-1 save_roc_curve=True window_size=100 stride=100 eval_stride=100 batch_size=1 eval_batch_size=1 normalization=None model=AnomalyTransformer model.anomaly_ratio=0.5 infer_options=["offline"] thresholding=off_f1_best &&
  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED dataset=SMD +dataset_id=machine-2-1 save_roc_curve=True window_size=100 stride=100 eval_stride=100 batch_size=1 eval_batch_size=1 normalization=None model=AnomalyTransformer model.anomaly_ratio=0.5 infer_options=["offline"] thresholding=q99 &&

  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED dataset=MSL +dataset_id=P-15 save_roc_curve=True window_size=100 stride=100 eval_stride=100 batch_size=1 eval_batch_size=1 normalization=None model=AnomalyTransformer model.anomaly_ratio=1.0  infer_options=["offline"] thresholding=off_f1_best &&
  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED dataset=MSL +dataset_id=P-15 save_roc_curve=True window_size=100 stride=100 eval_stride=100 batch_size=1 eval_batch_size=1 normalization=None model=AnomalyTransformer model.anomaly_ratio=1.0  infer_options=["offline"] thresholding=q100 &&

  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED dataset=SMAP +dataset_id=T-3 save_roc_curve=True window_size=100 stride=100 eval_stride=100 batch_size=1 eval_batch_size=1 normalization=None model=AnomalyTransformer model.anomaly_ratio=1.0  infer_options=["offline"] thresholding=off_f1_best &&
  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED dataset=SMAP +dataset_id=T-3 save_roc_curve=True window_size=100 stride=100 eval_stride=100 batch_size=1 eval_batch_size=1 normalization=None model=AnomalyTransformer model.anomaly_ratio=1.0  infer_options=["offline"] thresholding=q99 &&

  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED dataset=CreditCard save_roc_curve=True window_size=100 stride=100 eval_stride=100 batch_size=256 eval_batch_size=256 normalization=None model=AnomalyTransformer model.anomaly_ratio=0.5  infer_options=["offline"] thresholding=off_f1_best &&

  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED dataset=yahoo +dataset_id=real_20 save_roc_curve=True window_size=100 stride=100 eval_stride=100 batch_size=1 eval_batch_size=1 normalization=None model=AnomalyTransformer model.anomaly_ratio=0.5  infer_options=["offline"] thresholding=off_f1_best &&
  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED dataset=yahoo +dataset_id=real_20 save_roc_curve=True window_size=100 stride=100 eval_stride=100 batch_size=1 eval_batch_size=1 normalization=None model=AnomalyTransformer model.anomaly_ratio=0.5  infer_options=["offline"] thresholding=q98 &&

  CUDA_VISIBLE_DEVICES=$1 python test.py SEED=$SEED dataset=yahoo +dataset_id=real_55 save_roc_curve=True window_size=100 stride=100 eval_stride=100 batch_size=1 eval_batch_size=1 normalization=None model=AnomalyTransformer model.anomaly_ratio=0.5  infer_options=["offline"] thresholding=off_f1_best
done