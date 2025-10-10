# 🎨 Ejemplos de Integración Frontend - CV Recommendation API

## 📋 Tabla de Contenidos
1. [Setup Inicial](#setup-inicial)
2. [React/Next.js Examples](#reactnextjs-examples)
3. [Vue.js Examples](#vuejs-examples)
4. [Componentes Sugeridos](#componentes-sugeridos)
5. [State Management](#state-management)

---

## 🚀 Setup Inicial

### API Client (TypeScript)

```typescript
// lib/api-client.ts
const API_BASE_URL = 'http://localhost:8000';

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options?: RequestInit
  ): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers: {
        ...options?.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'API Error');
    }

    return response.json();
  }

  // CVs
  async uploadCV(file: File) {
    const formData = new FormData();
    formData.append('cv_file', file);

    return this.request<{
      success: boolean;
      cv_id: number;
      nombre: string;
      email: string;
      telefono: string;
      ubicacion: string;
      message: string;
    }>('/cvs', {
      method: 'POST',
      body: formData,
    });
  }

  async getCVs(skip = 0, limit = 100) {
    return this.request<Array<{
      id: number;
      nombre: string;
      email: string;
      ubicacion: string;
      created_at: string;
    }>>(`/cvs?skip=${skip}&limit=${limit}`);
  }

  async getCV(id: number) {
    return this.request<{
      id: number;
      nombre: string;
      email: string;
      telefono: string;
      ubicacion: string;
      cv_data: any;
      created_at: string;
    }>(`/cvs/${id}`);
  }

  async deleteCV(id: number) {
    return this.request<{ message: string }>(`/cvs/${id}`, {
      method: 'DELETE',
    });
  }

  async searchCVs(nombre: string) {
    return this.request<Array<{
      id: number;
      nombre: string;
      email: string;
      created_at: string;
    }>>(`/cvs/search/${nombre}`);
  }

  // Jobs
  async createJob(description: string) {
    const formData = new FormData();
    formData.append('description', description);

    return this.request<{
      success: boolean;
      job_id: number;
      titulo: string;
      empresa: string;
      ubicacion: string;
      modalidad: string;
      message: string;
    }>('/jobs', {
      method: 'POST',
      body: formData,
    });
  }

  async getJobs(skip = 0, limit = 100) {
    return this.request<Array<{
      id: number;
      titulo: string;
      empresa: string;
      ubicacion: string;
      created_at: string;
    }>>(`/jobs?skip=${skip}&limit=${limit}`);
  }

  async getJob(id: number) {
    return this.request<{
      id: number;
      titulo: string;
      empresa: string;
      ubicacion: string;
      job_data: any;
      created_at: string;
    }>(`/jobs/${id}`);
  }

  async deleteJob(id: number) {
    return this.request<{ message: string }>(`/jobs/${id}`, {
      method: 'DELETE',
    });
  }

  // Analysis
  async analyze(
    cvId: number,
    jobId: number,
    weights?: {
      experience?: number;
      technical_skills?: number;
      education?: number;
      responsibilities?: number;
      certifications?: number;
      soft_skills?: number;
      languages?: number;
      location?: number;
    }
  ) {
    return this.request<{
      success: boolean;
      analysis_id: number;
      cv_id: number;
      job_id: number;
      candidato: string;
      trabajo: string;
      score: number;
      score_porcentaje: number;
      score_breakdown: any;
      weights_used: any;
      processing_time: number;
    }>(`/analyze/${cvId}/${jobId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: weights ? JSON.stringify(weights) : null,
    });
  }

  async getAnalyses(skip = 0, limit = 100) {
    return this.request<Array<{
      id: number;
      cv_id: number;
      job_id: number;
      candidato: string;
      trabajo: string;
      score_porcentaje: number;
      created_at: string;
    }>>(`/analyses?skip=${skip}&limit=${limit}`);
  }

  async getAnalysis(id: number) {
    return this.request<{
      id: number;
      cv_id: number;
      job_id: number;
      candidato: string;
      trabajo: string;
      score: number;
      score_porcentaje: number;
      score_breakdown: any;
      resultado_completo: any;
      processing_time: number;
      created_at: string;
    }>(`/analyses/${id}`);
  }

  async getCVAnalyses(cvId: number) {
    return this.request<Array<{
      id: number;
      job_id: number;
      trabajo: string;
      score_porcentaje: number;
      created_at: string;
    }>>(`/cvs/${cvId}/analyses`);
  }

  async getJobAnalyses(jobId: number) {
    return this.request<Array<{
      id: number;
      cv_id: number;
      candidato: string;
      score_porcentaje: number;
      created_at: string;
    }>>(`/jobs/${jobId}/analyses`);
  }

  async getTopCandidates(jobId: number, limit = 10) {
    return this.request<Array<{
      rank: number;
      analysis_id: number;
      cv_id: number;
      candidato: string;
      score_porcentaje: number;
      created_at: string;
    }>>(`/jobs/${jobId}/top-candidatos?limit=${limit}`);
  }

  async getStats() {
    return this.request<{
      total_cvs: number;
      total_jobs: number;
      total_analyses: number;
      score_promedio: number;
      score_promedio_porcentaje: number;
    }>('/stats');
  }
}

export const apiClient = new ApiClient();
```

---

## ⚛️ React/Next.js Examples

### 1. Upload CV Component

```tsx
// components/CVUploader.tsx
'use client';

import { useState } from 'react';
import { apiClient } from '@/lib/api-client';

export default function CVUploader() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);

    try {
      const response = await apiClient.uploadCV(file);
      setResult(response);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto p-6">
      <h2 className="text-2xl font-bold mb-4">Subir CV</h2>
      
      <input
        type="file"
        accept=".pdf"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
        className="mb-4 block w-full text-sm"
      />

      <button
        onClick={handleUpload}
        disabled={!file || loading}
        className="w-full bg-blue-500 text-white py-2 px-4 rounded disabled:bg-gray-300"
      >
        {loading ? 'Procesando...' : 'Subir CV'}
      </button>

      {error && (
        <div className="mt-4 p-4 bg-red-100 text-red-700 rounded">
          {error}
        </div>
      )}

      {result && (
        <div className="mt-4 p-4 bg-green-100 rounded">
          <p className="font-bold">{result.nombre}</p>
          <p className="text-sm text-gray-600">{result.email}</p>
          <p className="text-sm text-gray-600">{result.ubicacion}</p>
          <p className="text-xs text-green-700 mt-2">CV ID: {result.cv_id}</p>
        </div>
      )}
    </div>
  );
}
```

### 2. Analysis Component with Weights

```tsx
// components/CVAnalyzer.tsx
'use client';

import { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api-client';

const WEIGHT_PRESETS = {
  default: {
    experience: 0.30,
    technical_skills: 0.15,
    education: 0.15,
    responsibilities: 0.15,
    certifications: 0.10,
    soft_skills: 0.08,
    languages: 0.04,
    location: 0.03,
  },
  junior: {
    education: 0.35,
    technical_skills: 0.25,
    certifications: 0.15,
    experience: 0.15,
    soft_skills: 0.10,
  },
  senior: {
    experience: 0.40,
    technical_skills: 0.30,
    certifications: 0.15,
    education: 0.10,
    soft_skills: 0.05,
  },
  manager: {
    experience: 0.35,
    soft_skills: 0.25,
    responsibilities: 0.20,
    education: 0.10,
    technical_skills: 0.10,
  },
};

export default function CVAnalyzer() {
  const [cvs, setCvs] = useState<any[]>([]);
  const [jobs, setJobs] = useState<any[]>([]);
  const [selectedCV, setSelectedCV] = useState<number | null>(null);
  const [selectedJob, setSelectedJob] = useState<number | null>(null);
  const [preset, setPreset] = useState<keyof typeof WEIGHT_PRESETS>('default');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    const [cvsData, jobsData] = await Promise.all([
      apiClient.getCVs(),
      apiClient.getJobs(),
    ]);
    setCvs(cvsData);
    setJobs(jobsData);
  };

  const handleAnalyze = async () => {
    if (!selectedCV || !selectedJob) return;

    setLoading(true);
    try {
      const weights = WEIGHT_PRESETS[preset];
      const response = await apiClient.analyze(selectedCV, selectedJob, weights);
      setResult(response);
    } catch (err: any) {
      alert(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-6">Análisis CV vs Job</h2>

      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <label className="block text-sm font-medium mb-2">Seleccionar CV</label>
          <select
            value={selectedCV || ''}
            onChange={(e) => setSelectedCV(Number(e.target.value))}
            className="w-full border rounded p-2"
          >
            <option value="">Seleccione un CV</option>
            {cvs.map((cv) => (
              <option key={cv.id} value={cv.id}>
                {cv.nombre} - {cv.email}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Seleccionar Job</label>
          <select
            value={selectedJob || ''}
            onChange={(e) => setSelectedJob(Number(e.target.value))}
            className="w-full border rounded p-2"
          >
            <option value="">Seleccione un Job</option>
            {jobs.map((job) => (
              <option key={job.id} value={job.id}>
                {job.titulo} - {job.empresa}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">Perfil de Pesos</label>
        <div className="flex gap-2">
          <button
            onClick={() => setPreset('default')}
            className={`px-4 py-2 rounded ${preset === 'default' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
          >
            Default
          </button>
          <button
            onClick={() => setPreset('junior')}
            className={`px-4 py-2 rounded ${preset === 'junior' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
          >
            Junior
          </button>
          <button
            onClick={() => setPreset('senior')}
            className={`px-4 py-2 rounded ${preset === 'senior' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
          >
            Senior
          </button>
          <button
            onClick={() => setPreset('manager')}
            className={`px-4 py-2 rounded ${preset === 'manager' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
          >
            Manager
          </button>
        </div>
      </div>

      <button
        onClick={handleAnalyze}
        disabled={!selectedCV || !selectedJob || loading}
        className="w-full bg-green-500 text-white py-3 px-4 rounded disabled:bg-gray-300 mb-6"
      >
        {loading ? 'Analizando...' : 'Analizar'}
      </button>

      {result && (
        <div className="bg-white border rounded-lg p-6">
          <h3 className="text-xl font-bold mb-4">Resultado del Análisis</h3>
          
          <div className="grid grid-cols-2 gap-4 mb-6">
            <div>
              <p className="text-sm text-gray-600">Candidato</p>
              <p className="font-semibold">{result.candidato}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Trabajo</p>
              <p className="font-semibold">{result.trabajo}</p>
            </div>
          </div>

          <div className="text-center mb-6">
            <div className="text-6xl font-bold text-blue-600">
              {result.score_porcentaje}%
            </div>
            <p className="text-gray-600">Score de Compatibilidad</p>
          </div>

          <div className="space-y-2">
            <h4 className="font-semibold mb-3">Desglose por Aspecto</h4>
            {Object.entries(result.score_breakdown).map(([key, value]: [string, any]) => (
              <div key={key} className="flex items-center justify-between">
                <span className="text-sm capitalize">{key.replace('_', ' ')}</span>
                <div className="flex items-center gap-2">
                  <div className="w-32 bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-500 h-2 rounded-full"
                      style={{ width: `${value.score * 100}%` }}
                    />
                  </div>
                  <span className="text-sm font-medium w-12 text-right">
                    {(value.score * 100).toFixed(0)}%
                  </span>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-4 text-xs text-gray-500">
            <p>Tiempo de procesamiento: {result.processing_time}s</p>
            <p>ID del análisis: {result.analysis_id}</p>
          </div>
        </div>
      )}
    </div>
  );
}
```

### 3. Top Candidates Component

```tsx
// components/TopCandidates.tsx
'use client';

import { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api-client';

export default function TopCandidates({ jobId }: { jobId: number }) {
  const [candidates, setCandidates] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [limit, setLimit] = useState(10);

  useEffect(() => {
    loadCandidates();
  }, [jobId, limit]);

  const loadCandidates = async () => {
    setLoading(true);
    try {
      const data = await apiClient.getTopCandidates(jobId, limit);
      setCandidates(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Cargando...</div>;

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">Top Candidatos</h2>
        <select
          value={limit}
          onChange={(e) => setLimit(Number(e.target.value))}
          className="border rounded p-2"
        >
          <option value={5}>Top 5</option>
          <option value={10}>Top 10</option>
          <option value={20}>Top 20</option>
        </select>
      </div>

      <div className="space-y-4">
        {candidates.map((candidate, idx) => (
          <div
            key={candidate.analysis_id}
            className={`p-4 rounded-lg border-2 ${
              idx === 0
                ? 'bg-yellow-50 border-yellow-400'
                : idx === 1
                ? 'bg-gray-50 border-gray-400'
                : idx === 2
                ? 'bg-orange-50 border-orange-400'
                : 'bg-white border-gray-200'
            }`}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div
                  className={`text-3xl font-bold ${
                    idx === 0
                      ? 'text-yellow-600'
                      : idx === 1
                      ? 'text-gray-600'
                      : idx === 2
                      ? 'text-orange-600'
                      : 'text-gray-400'
                  }`}
                >
                  #{candidate.rank}
                </div>
                <div>
                  <p className="font-semibold text-lg">{candidate.candidato}</p>
                  <p className="text-sm text-gray-600">CV ID: {candidate.cv_id}</p>
                </div>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-blue-600">
                  {candidate.score_porcentaje}%
                </div>
                <p className="text-xs text-gray-500">
                  {new Date(candidate.created_at).toLocaleDateString()}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
```

### 4. Dashboard Component

```tsx
// components/Dashboard.tsx
'use client';

import { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api-client';

export default function Dashboard() {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const data = await apiClient.getStats();
      setStats(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Cargando...</div>;

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-8">Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-blue-500 text-white p-6 rounded-lg">
          <p className="text-sm opacity-80">Total CVs</p>
          <p className="text-4xl font-bold">{stats.total_cvs}</p>
        </div>

        <div className="bg-green-500 text-white p-6 rounded-lg">
          <p className="text-sm opacity-80">Total Jobs</p>
          <p className="text-4xl font-bold">{stats.total_jobs}</p>
        </div>

        <div className="bg-purple-500 text-white p-6 rounded-lg">
          <p className="text-sm opacity-80">Total Análisis</p>
          <p className="text-4xl font-bold">{stats.total_analyses}</p>
        </div>

        <div className="bg-orange-500 text-white p-6 rounded-lg">
          <p className="text-sm opacity-80">Score Promedio</p>
          <p className="text-4xl font-bold">
            {stats.score_promedio_porcentaje.toFixed(1)}%
          </p>
        </div>
      </div>
    </div>
  );
}
```

---

## 🟢 Vue.js Examples

### Composable for API

```typescript
// composables/useApi.ts
import { ref } from 'vue';

const API_BASE_URL = 'http://localhost:8000';

export function useApi() {
  const loading = ref(false);
  const error = ref<string | null>(null);

  const request = async <T>(endpoint: string, options?: RequestInit): Promise<T> => {
    loading.value = true;
    error.value = null;

    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'API Error');
      }

      return await response.json();
    } catch (err: any) {
      error.value = err.message;
      throw err;
    } finally {
      loading.value = false;
    }
  };

  return {
    loading,
    error,
    request,
  };
}
```

### Vue Component Example

```vue
<!-- components/CVAnalyzer.vue -->
<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useApi } from '@/composables/useApi';

const { loading, error, request } = useApi();

const cvs = ref<any[]>([]);
const jobs = ref<any[]>([]);
const selectedCV = ref<number | null>(null);
const selectedJob = ref<number | null>(null);
const result = ref<any>(null);

const weights = ref({
  experience: 0.30,
  technical_skills: 0.15,
  education: 0.15,
  responsibilities: 0.15,
  certifications: 0.10,
  soft_skills: 0.08,
  languages: 0.04,
  location: 0.03,
});

onMounted(async () => {
  cvs.value = await request('/cvs');
  jobs.value = await request('/jobs');
});

const analyze = async () => {
  if (!selectedCV.value || !selectedJob.value) return;

  result.value = await request(
    `/analyze/${selectedCV.value}/${selectedJob.value}`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(weights.value),
    }
  );
};
</script>

<template>
  <div class="analyzer">
    <h2>Análisis CV vs Job</h2>

    <select v-model="selectedCV">
      <option :value="null">Seleccione un CV</option>
      <option v-for="cv in cvs" :key="cv.id" :value="cv.id">
        {{ cv.nombre }} - {{ cv.email }}
      </option>
    </select>

    <select v-model="selectedJob">
      <option :value="null">Seleccione un Job</option>
      <option v-for="job in jobs" :key="job.id" :value="job.id">
        {{ job.titulo }} - {{ job.empresa }}
      </option>
    </select>

    <button @click="analyze" :disabled="!selectedCV || !selectedJob || loading">
      {{ loading ? 'Analizando...' : 'Analizar' }}
    </button>

    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="result" class="result">
      <h3>Resultado</h3>
      <p>Score: {{ result.score_porcentaje }}%</p>
      <p>Candidato: {{ result.candidato }}</p>
      <p>Trabajo: {{ result.trabajo }}</p>
    </div>
  </div>
</template>
```

---

## 🎨 Componentes Sugeridos

### 1. CVList
- Lista paginada de CVs
- Búsqueda por nombre
- Acciones: Ver, Eliminar, Analizar

### 2. JobList
- Lista paginada de Jobs
- Búsqueda por título
- Acciones: Ver, Eliminar, Ver Candidatos

### 3. AnalysisViewer
- Visualización detallada de análisis
- Gráficos de radar/barras
- Exportar a PDF

### 4. WeightConfigurator
- Sliders para ajustar pesos
- Presets (Junior, Senior, Manager)
- Validación de suma = 1.0

### 5. ScoreGauge
- Gauge circular para score
- Colores según rango
- Animación

### 6. ComparisonTable
- Comparar múltiples candidatos
- Ordenar por aspecto
- Destacar mejor en cada categoría

---

## 🗂️ State Management

### Zustand (React)

```typescript
// store/useStore.ts
import create from 'zustand';

interface Store {
  cvs: any[];
  jobs: any[];
  analyses: any[];
  setCvs: (cvs: any[]) => void;
  setJobs: (jobs: any[]) => void;
  setAnalyses: (analyses: any[]) => void;
  addCV: (cv: any) => void;
  addJob: (job: any) => void;
  addAnalysis: (analysis: any) => void;
}

export const useStore = create<Store>((set) => ({
  cvs: [],
  jobs: [],
  analyses: [],
  setCvs: (cvs) => set({ cvs }),
  setJobs: (jobs) => set({ jobs }),
  setAnalyses: (analyses) => set({ analyses }),
  addCV: (cv) => set((state) => ({ cvs: [...state.cvs, cv] })),
  addJob: (job) => set((state) => ({ jobs: [...state.jobs, job] })),
  addAnalysis: (analysis) => set((state) => ({ analyses: [...state.analyses, analysis] })),
}));
```

### Pinia (Vue)

```typescript
// stores/app.ts
import { defineStore } from 'pinia';

export const useAppStore = defineStore('app', {
  state: () => ({
    cvs: [],
    jobs: [],
    analyses: [],
  }),
  actions: {
    setCvs(cvs: any[]) {
      this.cvs = cvs;
    },
    setJobs(jobs: any[]) {
      this.jobs = jobs;
    },
    setAnalyses(analyses: any[]) {
      this.analyses = analyses;
    },
    addCV(cv: any) {
      this.cvs.push(cv);
    },
    addJob(job: any) {
      this.jobs.push(job);
    },
    addAnalysis(analysis: any) {
      this.analyses.push(analysis);
    },
  },
});
```

---

## 📊 Visualización de Datos Recomendada

### Librerías Sugeridas

1. **Chart.js** / **Recharts** - Gráficos de barras y líneas
2. **ApexCharts** - Gráficos de radar para score_breakdown
3. **React Circular Progressbar** - Gauge para score
4. **Framer Motion** - Animaciones
5. **React Table** / **TanStack Table** - Tablas avanzadas

### Ejemplo con Recharts

```tsx
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';

function ScoreBreakdownChart({ breakdown }: { breakdown: any }) {
  const data = Object.entries(breakdown).map(([key, value]: [string, any]) => ({
    aspect: key.replace('_', ' '),
    score: value.score * 100,
  }));

  return (
    <RadarChart width={500} height={400} data={data}>
      <PolarGrid />
      <PolarAngleAxis dataKey="aspect" />
      <PolarRadiusAxis domain={[0, 100]} />
      <Radar dataKey="score" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.6} />
    </RadarChart>
  );
}
```

---

## ✅ Checklist de Implementación

- [ ] Configurar API client
- [ ] Implementar autenticación (si es necesario)
- [ ] Crear componente de upload de CV
- [ ] Crear formulario de Job
- [ ] Implementar módulo de análisis
- [ ] Configurador de pesos con presets
- [ ] Visualización de score con gauge
- [ ] Gráficos de score_breakdown
- [ ] Vista de ranking/top candidatos
- [ ] Dashboard con estadísticas
- [ ] Búsqueda y filtros
- [ ] Paginación
- [ ] Exportación a PDF
- [ ] Manejo de errores global
- [ ] Loading states
- [ ] Optimistic updates
- [ ] Cache de datos
- [ ] Responsive design
- [ ] Dark mode (opcional)

---

**Happy Coding!** 🚀

