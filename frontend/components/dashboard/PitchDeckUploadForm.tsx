'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { pitchDeckSchema, PitchDeckFormData } from '../../lib/validations';
import { useState } from 'react';
import { Upload, CheckCircle2, AlertCircle } from 'lucide-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';

export function PitchDeckUploadForm({ startupId }: { startupId: string }) {
  const [success, setSuccess] = useState(false);
  const queryClient = useQueryClient();
  
  const { register, handleSubmit, formState: { errors }, reset } = useForm<PitchDeckFormData>({
    resolver: zodResolver(pitchDeckSchema),
    defaultValues: {
      startup_id: startupId
    }
  });

  const mutation = useMutation({
    mutationFn: async (data: PitchDeckFormData) => {
      const formData = new FormData();
      formData.append('file', data.file[0]);
      formData.append('startup_id', data.startup_id);

      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000/api'}/ai/analyze-pitch-deck`, {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) throw new Error('Upload failed');
      return res.json();
    },
    onSuccess: () => {
      setSuccess(true);
      reset();
      queryClient.invalidateQueries({ queryKey: ['dashboard', 'founder', startupId] });
      setTimeout(() => setSuccess(false), 5000);
    },
  });

  const onSubmit = (data: PitchDeckFormData) => {
    mutation.mutate(data);
  };

  return (
    <div className="panel" style={{ marginTop: 16 }}>
      <h3>Upload Pitch Deck</h3>
      <p className="muted">Upload your pitch deck in PDF format (max 10MB) for AI analysis.</p>
      
      <form onSubmit={handleSubmit(onSubmit)} className="list" style={{ marginTop: 16 }}>
        <input type="hidden" {...register('startup_id')} />
        
        <div className="card" style={{ border: errors.file ? '1px solid #ef4444' : '1px dashed #334155', padding: '24px', textAlign: 'center' }}>
          <Upload className="mx-auto mb-2 opacity-50" size={32} />
          <input 
            type="file" 
            accept=".pdf" 
            {...register('file')} 
            className="block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-cyan-500 file:text-white hover:file:bg-cyan-600"
          />
          {errors.file && <p className="text-red-500 text-sm mt-2">{errors.file.message as string}</p>}
        </div>

        <button 
          type="submit" 
          disabled={mutation.isPending}
          className="btn btn-primary"
          style={{ width: '100%', marginTop: 8 }}
        >
          {mutation.isPending ? 'Uploading & Analyzing...' : 'Start AI Analysis'}
        </button>

        {success && (
          <div className="flex items-center gap-2 mt-4 text-emerald-400">
            <CheckCircle2 size={18} />
            <span>Pitch deck uploaded successfully! Analysis is starting.</span>
          </div>
        )}

        {mutation.isError && (
          <div className="flex items-center gap-2 mt-4 text-red-500">
            <AlertCircle size={18} />
            <span>Error: {mutation.error.message}</span>
          </div>
        )}
      </form>
    </div>
  );
}
