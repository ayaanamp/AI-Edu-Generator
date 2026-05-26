import React, { useState, useRef, useEffect } from 'react';
import { 
  Upload, 
  FileText, 
  Brain, 
  Volume2, 
  CheckCircle2, 
  XCircle, 
  ChevronRight, 
  RefreshCw, 
  Trophy, 
  Loader2,
  BarChart3, 
  Clock, 
  Sparkles, 
  Terminal, 
  Github, 
  BookOpen, 
  Play, 
  Pause, 
  RotateCcw, 
  ListTodo, 
  Circle, 
  Coffee, 
  FileCode,
  Check
} from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

// --- Utils ---
function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// --- Types ---
interface Keycard {
  id: string;
  text: string;
}

interface MCQ {
  id: string;
  question: string;
  options: string[];
  correctAnswer: number;
}

interface StudyData {
  keycards: Keycard[];
  mcqs: MCQ[];
}

// --- Components ---

const Header = ({ 
  filename, 
  activeTab, 
  onActiveTabChange 
}: { 
  filename: string | null;
  activeTab: 'study' | 'dashboard';
  onActiveTabChange: (tab: 'study' | 'dashboard') => void;
}) => (
  <header className="flex items-center justify-between px-8 py-4 border-b border-white/10 bg-[#0f0f0f] sticky top-0 z-50 print:hidden">
    <div className="flex items-center gap-3">
      <div className="w-8 h-8 bg-emerald-500 rounded-lg flex items-center justify-center shadow-[0_0_15px_rgba(16,185,129,0.3)] flex-shrink-0">
        <Brain className="w-5 h-5 text-black" />
      </div>
      <h1 className="text-xl font-semibold tracking-tight text-white font-sans">
        Lumina<span className="text-emerald-500 italic font-serif">AI</span> Study
      </h1>
    </div>
    <div className="flex items-center gap-4">
      {/* Dynamic Workspace Navigation Button */}
      <button
        onClick={() => onActiveTabChange(activeTab === 'study' ? 'dashboard' : 'study')}
        className={cn(
          "px-4 py-2 rounded-xl text-[10px] uppercase tracking-wider font-bold transition-all duration-300 flex items-center gap-2 border cursor-pointer",
          activeTab === 'dashboard'
            ? "bg-emerald-500 text-black border-emerald-500 shadow-[0_0_15px_rgba(16,185,129,0.4)]"
            : "bg-white/5 text-emerald-400 border-emerald-500/20 hover:bg-emerald-500/10 hover:border-emerald-500/30"
        )}
      >
        <Trophy className="w-3.5 h-3.5" />
        {activeTab === 'dashboard' ? "Active Study App" : "📊 Study Dashboard"}
      </button>

      {filename && activeTab === 'study' && (
        <div className="hidden md:flex items-center gap-2">
          <span className="text-[10px] uppercase tracking-widest text-white/40 font-bold">Document:</span>
          <span className="text-[10px] font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20 uppercase">
            {filename}
          </span>
        </div>
      )}
      <div className="w-8 h-8 rounded-full bg-white/5 border border-white/10 flex items-center justify-center text-xs font-serif italic text-white/60">
        AI
      </div>
    </div>
  </header>
);

const FileUpload = ({ onUpload, isLoading, error }: { onUpload: (file: File) => void, isLoading: boolean, error: string | null }) => {
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.[0]) onUpload(e.target.files[0]);
  };

  return (
    <div 
      className={cn(
        "relative group cursor-pointer border border-dashed rounded-3xl p-12 transition-all duration-500 flex flex-col items-center justify-center gap-6 min-h-[400px] overflow-hidden",
        isDragging ? "border-emerald-500 bg-emerald-500/5 shadow-[0_0_30px_rgba(16,185,129,0.1)]" : "border-white/10 bg-white/[0.02] hover:bg-white/[0.04] hover:border-white/20"
      )}
      onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={(e) => {
        e.preventDefault();
        setIsDragging(false);
        if (e.dataTransfer.files?.[0]) onUpload(e.dataTransfer.files[0]);
      }}
      onClick={() => fileInputRef.current?.click()}
    >
      <div className="absolute inset-0 bg-gradient-to-b from-transparent to-black/20 pointer-events-none" />
      <input type="file" ref={fileInputRef} onChange={handleFileChange} accept=".pdf" className="hidden" />
      
      <div className={cn(
        "w-20 h-20 rounded-full flex items-center justify-center transition-all duration-700 relative z-10",
        isLoading ? "bg-white/5" : "bg-emerald-500 shadow-[0_0_20px_rgba(16,185,129,0.4)] group-hover:scale-110"
      )}>
        {isLoading ? (
          <Loader2 className="w-10 h-10 text-emerald-500 animate-spin" />
        ) : (
          <Upload className="w-8 h-8 text-black" />
        )}
      </div>

      <div className="text-center relative z-10">
        <h3 className="text-2xl font-serif italic text-white/90 mb-2">
          {isLoading ? "Synthesizing Knowledge..." : "Source Acquisition"}
        </h3>
        <p className="text-sm text-white/40 font-sans max-w-[280px] leading-relaxed mx-auto">
          {isLoading ? "The intelligence engine is mapping neural paths from your source material." : "Deploy your PDF document to initiate high-fidelity extraction and quiz generation."}
        </p>
      </div>

      {error && (
        <motion.div 
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="relative z-10 flex items-center gap-3 px-6 py-4 bg-red-500/10 border border-red-500/20 rounded-2xl max-w-sm"
        >
          <XCircle className="w-5 h-5 text-red-500 shrink-0" />
          <div className="text-left">
            <p className="text-[10px] uppercase tracking-widest font-bold text-red-400 mb-0.5">Pipeline Error</p>
            <p className="text-xs text-red-100/70 leading-relaxed font-sans">{error}</p>
          </div>
        </motion.div>
      )}
      
      {!isLoading && (
        <div className="mt-4 flex items-center justify-center gap-2 opacity-50 group-hover:opacity-100 transition-opacity">
          <div className="h-px w-8 bg-white/10" />
          <span className="text-[10px] uppercase tracking-[0.3em] font-bold text-white/30">
            {error ? "Deploy Different Document" : "Drag to Deploy"}
          </span>
          <div className="h-px w-8 bg-white/10" />
        </div>
      )}
    </div>
  );
};

const KeycardList = ({ cards }: { cards: Keycard[] }) => {
  const [playingId, setPlayingId] = useState<string | null>(null);

  const playVoice = async (text: string, id: string) => {
    if (playingId) return;
    setPlayingId(id);
    try {
      const res = await fetch('/api/tts', {
         method: 'POST',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify({ text })
      });
      
      if (res.status === 204) {
        console.log("Falling back to SpeechSynthesis");
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.onend = () => setPlayingId(null);
        utterance.onerror = () => setPlayingId(null);
        window.speechSynthesis.speak(utterance);
        return;
      }

      const data = await res.json();
      if (data.audio) {
        const byteCharacters = atob(data.audio);
        const byteNumbers = new Array(byteCharacters.length);
        for (let i = 0; i < byteCharacters.length; i++) {
          byteNumbers[i] = byteCharacters.charCodeAt(i);
        }
        const byteArray = new Uint8Array(byteNumbers);
        const blob = new Blob([byteArray], { type: data.mimeType || 'audio/wav' });
        const url = URL.createObjectURL(blob);
        
        const audio = new Audio(url);
        audio.onended = () => {
          setPlayingId(null);
          URL.revokeObjectURL(url);
        };
        audio.onerror = (e) => {
          console.error("Audio playback error:", e);
          setPlayingId(null);
          URL.revokeObjectURL(url);
        };
        await audio.play();
      } else {
        throw new Error("No audio data received");
      }
    } catch (error) {
      console.error("Voice playback error:", error);
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.onend = () => setPlayingId(null);
      window.speechSynthesis.speak(utterance);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
        <h2 className="text-3xl font-serif italic text-white/90">Extracted Keycards</h2>
        <span className="text-[10px] text-white/40 font-mono tracking-widest uppercase">
          {cards.length} INSIGHTS DISCOVERED
        </span>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {cards.map((card, idx) => (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1 }}
            key={card.id}
            className="p-8 bg-[#151515] border border-white/5 rounded-3xl relative group hover:border-emerald-500/20 transition-all duration-300 shadow-2xl"
          >
            <span className="absolute top-6 right-8 text-[44px] font-serif italic text-white/5 select-none leading-none pointer-events-none group-hover:text-emerald-500/5 transition-colors">
              {(idx + 1).toString().padStart(2, '0')}
            </span>
            <p className="text-emerald-400 text-[10px] font-mono mb-4 uppercase tracking-[0.2em] font-bold">Foundation Fact</p>
            <p className="text-white/90 leading-relaxed text-xl font-light mb-8 pr-4">{card.text}</p>
            <button 
              onClick={() => playVoice(card.text, card.id)}
              disabled={playingId !== null}
              className={cn(
                "flex items-center gap-2 px-4 py-2 rounded-full text-[10px] uppercase tracking-widest font-bold transition-all duration-300",
                playingId === card.id 
                  ? "bg-emerald-500 text-black shadow-[0_0_15px_rgba(16,185,129,0.4)]" 
                  : "bg-white/5 text-white/40 hover:bg-white/10 hover:text-white"
              )}
            >
              <Volume2 className={cn("w-3.5 h-3.5", playingId === card.id && "animate-pulse")} />
              {playingId === card.id ? "Synthesizing..." : "Play Audio"}
            </button>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

const Quiz = ({ mcqs, onRestart }: { mcqs: MCQ[], onRestart: () => void }) => {
  const [currentIdx, setCurrentIdx] = useState(0);
  const [selectedIdx, setSelectedIdx] = useState<number | null>(null);
  const [score, setScore] = useState(0);
  const [isFinished, setIsFinished] = useState(false);
  const [shuffledOptions, setShuffledOptions] = useState<{ text: string, originalIdx: number }[]>([]);

  useEffect(() => {
    if (currentIdx < mcqs.length) {
      const current = mcqs[currentIdx];
      const items = current.options.map((opt, i) => ({ text: opt, originalIdx: i }));
      setShuffledOptions(items);
      setSelectedIdx(null);
    }
  }, [currentIdx, mcqs]);

  if (isFinished) {
    return (
      <div className="flex flex-col items-center justify-center p-16 text-center bg-white/[0.02] rounded-[3rem] border border-white/5 shadow-2xl relative overflow-hidden">
        <div className="absolute inset-x-0 top-0 h-1 bg-gradient-to-r from-transparent via-emerald-500 to-transparent opacity-50" />
        <div className="w-24 h-24 bg-emerald-500 rounded-[2rem] flex items-center justify-center mb-8 shadow-[0_0_30px_rgba(16,185,129,0.2)]">
          <Trophy className="w-12 h-12 text-black" />
        </div>
        <h2 className="text-4xl font-serif italic text-white mb-4">Neural Map Complete</h2>
        <p className="text-xl text-white/50 mb-12 font-light">
          Knowledge retention score: <span className="text-emerald-400 font-mono font-bold tracking-tighter">{(score / mcqs.length * 100).toFixed(0)}%</span>
          <br/>
          <span className="text-xs uppercase tracking-[0.2em] mt-2 block opacity-50">{score} of {mcqs.length} correct responses</span>
        </p>
        <button 
          onClick={onRestart}
          className="px-10 py-4 bg-white text-black font-bold text-xs uppercase tracking-widest rounded-2xl hover:bg-emerald-400 transition-all duration-300 active:scale-95 shadow-xl shadow-black/50"
        >
          Reset Session
        </button>
      </div>
    );
  }

  const current = mcqs[currentIdx];

  const handleSelect = (idx: number) => {
    if (selectedIdx !== null) return;
    setSelectedIdx(idx);
    if (shuffledOptions[idx].originalIdx === current.correctAnswer) {
      setScore(s => s + 1);
    }
  };

  const nextQuestion = () => {
    if (currentIdx + 1 < mcqs.length) {
      setCurrentIdx(c => c + 1);
    } else {
      setIsFinished(true);
    }
  };

  return (
    <div className="max-w-3xl mx-auto flex flex-col min-h-[500px]">
      <div className="mb-6 flex items-center justify-between border-b border-white/10 pb-4">
        <h2 className="text-[10px] font-bold tracking-[0.3em] text-white/30 uppercase">Knowledge Assessment</h2>
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-3">
            <div className="h-1.5 w-32 bg-white/5 rounded-full overflow-hidden">
              <div 
                className="h-full bg-emerald-500 transition-all duration-1000" 
                style={{ width: `${((currentIdx + 1) / mcqs.length) * 100}%` }}
              />
            </div>
            <span className="text-[10px] font-mono text-emerald-400">STAGE {currentIdx + 1} / {mcqs.length}</span>
          </div>
          <div className="h-4 w-px bg-white/10 hidden sm:block" />
          <span className="text-[10px] font-mono text-white/40 uppercase tracking-widest hidden sm:block">POINTS: {score * 100}</span>
        </div>
      </div>

      <div className="flex-1 bg-white/[0.03] border border-white/5 rounded-[2.5rem] p-10 flex flex-col shadow-3xl relative">
        <div className="mb-10 overflow-hidden">
          <motion.span 
            key={currentIdx}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="inline-block px-4 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-[10px] text-emerald-400 uppercase tracking-[0.2em] font-bold mb-6"
          >
            Inquiry Matrix {currentIdx + 1}
          </motion.span>
          <motion.h3 
            key={`ques-${currentIdx}`}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="text-3xl font-serif italic leading-tight text-white/95"
          >
            {current.question}
          </motion.h3>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-auto">
          {shuffledOptions.map((option, idx) => {
            const isCorrect = option.originalIdx === current.correctAnswer;
            const isSelected = selectedIdx === idx;
            const showCorrection = selectedIdx !== null;

            return (
              <button
                key={idx}
                onClick={() => handleSelect(idx)}
                disabled={selectedIdx !== null}
                className={cn(
                  "group flex items-center justify-between p-6 rounded-2xl border transition-all duration-300 text-left relative overflow-hidden",
                  selectedIdx === null 
                    ? "bg-white/[0.03] border-white/5 hover:border-emerald-500/30 hover:bg-white/[0.05]" 
                    : (isCorrect 
                        ? "bg-emerald-500/20 border-emerald-500 text-emerald-400" 
                        : (isSelected ? "bg-red-500/10 border-red-500/50 text-red-400" : "bg-transparent border-white/5 opacity-30"))
                )}
              >
                <div className="flex items-center gap-4 relative z-10">
                  <span className={cn(
                    "w-7 h-7 rounded-lg flex items-center justify-center text-[10px] font-bold transition-colors",
                    selectedIdx === null ? "bg-white/5 text-white/40 group-hover:bg-emerald-500/20 group-hover:text-emerald-400" : (isCorrect ? "bg-emerald-500 text-black" : "bg-white/5 text-white/20")
                  )}>
                    {showCorrection && isCorrect ? "✓" : String.fromCharCode(65 + idx)}
                  </span>
                  <span className="text-sm font-medium leading-snug">{option.text}</span>
                </div>
              </button>
            );
          })}
        </div>

        <AnimatePresence>
          {selectedIdx !== null && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              className="mt-10 pt-6 border-t border-white/5 flex flex-col sm:flex-row justify-between items-center gap-4"
            >
              <p className="text-[10px] text-white/30 italic uppercase tracking-widest font-bold">
                Verification complete &middot; Proceed to next stage
              </p>
              <button
                onClick={nextQuestion}
                className="w-full sm:w-auto px-10 py-3.5 bg-white text-black font-bold text-xs uppercase tracking-widest rounded-xl hover:bg-emerald-400 transition-all active:scale-95 shadow-xl shadow-black/40"
              >
                Next Stage
              </button>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

// --- Consolidated Study Dashboard & Tutorial ---
interface StudyDashboardProps {
  keycardCount: number;
  quizScore: number;
  totalMcqs: number;
}

const StudyDashboard = ({ keycardCount, quizScore, totalMcqs }: StudyDashboardProps) => {
  const [timerMinutes, setTimerMinutes] = useState(25);
  const [timerSeconds, setTimerSeconds] = useState(0);
  const [timerIsActive, setTimerIsActive] = useState(false);
  const [timerMode, setTimerMode] = useState<'pomodoro' | 'shortBreak' | 'deepFocus'>('pomodoro');
  const [showCelebration, setShowCelebration] = useState(false);

  // Todo Items
  const [todos, setTodos] = useState([
    { id: '1', text: 'Upload syllabus or research PDF', completed: keycardCount > 0 },
    { id: '2', text: 'Review automatically generated keycards', completed: keycardCount > 0 },
    { id: '3', text: 'Synthesize audio voice overview', completed: false },
    { id: '4', text: 'Achieve >80% accuracy in interactive practice quiz', completed: quizScore > 0 },
    { id: '5', text: 'Acquire local download offline package', completed: false },
  ]);

  // Sync Todo item checklist
  useEffect(() => {
    setTodos(prev => prev.map(todo => {
      if (todo.id === '1' || todo.id === '2') {
        return { ...todo, completed: keycardCount > 0 };
      }
      if (todo.id === '4') {
        return { ...todo, completed: totalMcqs > 0 && (quizScore / totalMcqs) >= 0.8 };
      }
      return todo;
    }));
  }, [keycardCount, quizScore, totalMcqs]);

  // Focus Timer Logic
  useEffect(() => {
    let interval: any = null;
    if (timerIsActive) {
      interval = setInterval(() => {
        if (timerSeconds > 0) {
          setTimerSeconds(timerSeconds - 1);
        } else if (timerSeconds === 0) {
          if (timerMinutes === 0) {
            setTimerIsActive(false);
            setShowCelebration(true);
            setTimeout(() => setShowCelebration(false), 6000);
            resetTimer();
          } else {
            setTimerMinutes(timerMinutes - 1);
            setTimerSeconds(59);
          }
        }
      }, 1000);
    } else {
      clearInterval(interval);
    }
    return () => clearInterval(interval);
  }, [timerIsActive, timerMinutes, timerSeconds]);

  const toggleTimer = () => setTimerIsActive(!timerIsActive);
  
  const resetTimer = () => {
    setTimerIsActive(false);
    if (timerMode === 'pomodoro') setTimerMinutes(25);
    else if (timerMode === 'shortBreak') setTimerMinutes(5);
    else if (timerMode === 'deepFocus') setTimerMinutes(45);
    setTimerSeconds(0);
  };

  const handleModeChange = (mode: 'pomodoro' | 'shortBreak' | 'deepFocus') => {
    setTimerMode(mode);
    setTimerIsActive(false);
    if (mode === 'pomodoro') setTimerMinutes(25);
    else if (mode === 'shortBreak') setTimerMinutes(5);
    else if (mode === 'deepFocus') setTimerMinutes(45);
    setTimerSeconds(0);
  };

  const toggleTodo = (id: string) => {
    setTodos(todos.map(t => t.id === id ? { ...t, completed: !t.completed } : t));
  };

  return (
    <div className="space-y-10 pb-20 font-sans">
      
      {/* Celebration Notification Banner (Replaces alert to protect iframe sandbox constraints) */}
      <AnimatePresence>
        {showCelebration && (
          <motion.div 
            initial={{ opacity: 0, y: -50 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -50 }}
            className="fixed top-24 left-1/2 -translate-x-1/2 z-[100] px-6 py-4 bg-emerald-500 text-black font-bold uppercase tracking-widest text-xs rounded-2xl flex items-center gap-3 shadow-[0_0_30px_rgb(16,185,129,0.5)]"
          >
            <Trophy className="w-5 h-5 animate-bounce" />
            <span>Focus Session Finished! Take a well-deserved break.</span>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Top Welcome Title */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div>
          <span className="text-[10px] text-emerald-400 font-bold tracking-[0.25em] uppercase font-mono bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-500/20">
            Lumina Workspace Hub
          </span>
          <h2 className="text-3xl font-serif text-white mt-3">
            Your Cognitive Study Dashboard
          </h2>
          <p className="text-sm text-white/50 mt-2 max-w-xl">
            Analyze insights parsed from your textbooks, keep on task with our focus timers, and view visual analytics designed to maximize memory retention.
          </p>
        </div>

        <div className="flex items-center gap-3 bg-white/5 border border-white/10 px-4 py-2.5 rounded-2xl">
          <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" />
          <span className="text-[10px] uppercase font-mono tracking-widest text-white/70">Secure Session Analytics Active</span>
        </div>
      </div>

      {/* Main Grid: Left statistics, center timer, right targets */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* SECTION A: PERSISTENT BENTO METRICS */}
        <div className="space-y-6">
          <div className="bg-[#111] border border-white/10 p-6 rounded-3xl space-y-4 shadow-xl">
            <div className="flex items-center gap-2 text-emerald-400">
              <BarChart3 className="w-4 h-4" />
              <h3 className="text-xs font-bold tracking-widest uppercase font-mono">Cognitive Stats</h3>
            </div>
            
            <div className="grid grid-cols-2 gap-4 pt-2">
              <div className="bg-[#181818] p-4 rounded-2xl border border-white/5">
                <p className="text-[9px] uppercase tracking-wider text-white/40">Insights Loaded</p>
                <p className="text-2xl font-serif text-white font-bold mt-1">{keycardCount}</p>
                <p className="text-[9px] text-emerald-400 mt-2">Parsed from source</p>
              </div>

              <div className="bg-[#181818] p-4 rounded-2xl border border-white/5">
                <p className="text-[9px] uppercase tracking-wider text-white/40">Quiz Score</p>
                <p className="text-2xl font-serif text-white font-bold mt-1">
                  {totalMcqs > 0 ? `${quizScore}/${totalMcqs}` : '—'}
                </p>
                <p className="text-[9px] text-white/30 mt-2">
                  {totalMcqs > 0 ? `${((quizScore/totalMcqs) * 100).toFixed(0)}% accuracy` : 'No quiz taken yet'}
                </p>
              </div>

              <div className="bg-[#181818] p-4 rounded-2xl border border-white/5 col-span-2">
                <div className="flex justify-between items-center">
                  <div>
                    <p className="text-[9px] uppercase tracking-wider text-white/40">Continuous Streak</p>
                    <p className="text-xl font-serif text-emerald-400 font-bold mt-1">1 Day</p>
                  </div>
                  <div className="px-3 py-1.5 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-[9px] font-mono text-emerald-400">
                    MASTER SCENE
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-emerald-500/5 to-transparent border border-emerald-500/10 p-6 rounded-3xl space-y-3">
            <h4 className="text-[10px] text-emerald-400 font-bold uppercase tracking-wider font-mono flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5" /> High-Fidelity Synthetics
            </h4>
            <p className="text-[11px] text-white/50 leading-relaxed font-sans">
              Drag over files inside of the primary workspace to generate high-quality keycards and multiple choice evaluation tasks automatically.
            </p>
          </div>
        </div>

        {/* SECTION B: FOCUS TIMER HUB */}
        <div className="bg-[#111] border border-white/10 p-8 rounded-3xl flex flex-col justify-between shadow-xl min-h-[350px]">
          <div>
            <div className="flex justify-between items-center mb-6">
              <div className="flex items-center gap-2 text-emerald-400">
                <Clock className="w-4 h-4" />
                <h3 className="text-xs font-bold tracking-widest uppercase font-mono">Focus Timer</h3>
              </div>
              
              <div className="flex bg-white/5 p-0.5 rounded-lg border border-white/5">
                <button 
                  onClick={() => handleModeChange('pomodoro')}
                  className={`px-2.5 py-1 text-[9px] font-bold uppercase tracking-wider rounded transition-all ${timerMode === 'pomodoro' ? 'bg-emerald-500 text-black' : 'text-white/40'}`}
                >
                  Pomo
                </button>
                <button 
                  onClick={() => handleModeChange('deepFocus')}
                  className={`px-2.5 py-1 text-[9px] font-bold uppercase tracking-wider rounded transition-all ${timerMode === 'deepFocus' ? 'bg-emerald-500 text-black' : 'text-white/40'}`}
                >
                  Deep
                </button>
              </div>
            </div>

            <div className="text-center py-6">
              <span className="text-6xl font-mono tracking-tighter text-white font-bold block mb-2">
                {timerMinutes.toString().padStart(2, '0')}:{timerSeconds.toString().padStart(2, '0')}
              </span>
              <span className="text-[10px] text-emerald-400/80 font-mono tracking-[0.2em] uppercase">
                {timerMode === 'pomodoro' ? '🍅 POMODORO FLOW' : '🌌 DEEP FOCUS SESSION'}
              </span>
            </div>
          </div>

          <div className="space-y-6">
            <div className="flex justify-center items-center gap-4">
              <button 
                onClick={resetTimer}
                className="w-10 h-10 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 flex items-center justify-center text-white/60 hover:text-white transition-all"
              >
                <RotateCcw className="w-4 h-4" />
              </button>
              
              <button 
                onClick={toggleTimer}
                className="px-8 py-3.5 bg-emerald-500 font-bold text-xs uppercase tracking-widest text-black rounded-2xl hover:bg-emerald-400 transition-all shadow-md shadow-emerald-500/20 active:scale-95 flex items-center gap-2"
              >
                {timerIsActive ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
                {timerIsActive ? 'Pause Session' : 'Start Focus'}
              </button>
            </div>

            {/* Ambient player reference */}
            <div className="pt-4 border-t border-white/5 flex items-center justify-between">
              <span className="text-[10px] uppercase text-white/40 font-bold tracking-wider">Focus Sounds</span>
              <span className="text-[9px] text-white/30 italic">Playing offline lo-fi audio track streams</span>
            </div>
          </div>
        </div>

        {/* SECTION C: LESSON GOALS CHECKLIST */}
        <div className="bg-[#111] border border-white/10 p-8 rounded-3xl flex flex-col justify-between shadow-xl">
          <div>
            <div className="flex justify-between items-center mb-6">
              <div className="flex items-center gap-2 text-emerald-400">
                <ListTodo className="w-4 h-4" />
                <h3 className="text-xs font-bold tracking-widest uppercase font-mono">Workspace Milestones</h3>
              </div>
              <span className="text-[9px] font-mono text-emerald-400 font-bold bg-emerald-500/10 px-2.5 py-0.5 rounded border border-emerald-500/20">
                {todos.filter(t => t.completed).length} / {todos.length} DONE
              </span>
            </div>

            <div className="space-y-3">
              {todos.map(todo => (
                <button
                  key={todo.id}
                  onClick={() => toggleTodo(todo.id)}
                  className="w-full flex items-start gap-3.5 text-left p-2.5 rounded-xl hover:bg-white/[0.02] transition-colors group"
                >
                  <div className="mt-0.5 shrink-0">
                    {todo.completed ? (
                      <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                    ) : (
                      <Circle className="w-4 h-4 text-white/20 group-hover:text-white/40 transition-colors" />
                    )}
                  </div>
                  <span className={`text-xs text-justify font-sans leading-normal ${todo.completed ? 'text-white/30 line-through' : 'text-white/80 group-hover:text-white transition-colors'}`}>
                    {todo.text}
                  </span>
                </button>
              ))}
            </div>
          </div>

          <p className="text-[10px] text-white/30 leading-normal italic mt-6">
            * Checkboxes sync instantly when you upload study materials or complete quiz modules.
          </p>
        </div>

      </div>

      {/* SECTION 2: GITHUB EXPORT & LOCAL DEPLOYMENT WORKSHOP */}
      <div className="p-8 md:p-12 bg-white/[0.02] border border-white/5 rounded-[2.5rem]">
        <div className="max-w-4xl space-y-8">
          
          <div className="space-y-2 border-b border-white/15 pb-6">
            <span className="inline-block px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-[9px] font-mono text-emerald-400 tracking-wider uppercase font-bold">
              Engineering Deployment Manual
            </span>
            <h3 className="text-2xl font-serif text-white">How To Connect & Deploy On Your Machine</h3>
            <p className="text-sm text-white/50 leading-relaxed">
              Have you finished studying and need to submit this beautiful dashboard code to GitHub? Or maybe run the model completely offline in an air-gapped terminal using local AI networks? Use the definitive beginner guides below.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            
            <div className="space-y-4">
              <h4 className="font-serif italic text-white flex items-center gap-2">
                <Github className="w-4 h-4 text-emerald-400" /> GitHub Desktop Guide
              </h4>
              <p className="text-xs text-white/60 leading-relaxed font-sans">
                The safest visual workflow for uploading your code. Avoid typing console mistakes.
              </p>
              <ol className="text-xs text-white/50 space-y-3 pl-4 list-decimal leading-relaxed">
                <li>Download your project folder from your online Settings as a **ZIP file**.</li>
                <li>Download and open **GitHub Desktop** on your computer.</li>
                <li>Go to <strong className="text-white">File &rarr; Add Local Repository...</strong>, choose your unzipped root folder.</li>
                <li>If prompted, click **"create a repository"** inside this directory space.</li>
                <li>Type your initial update commit and click <strong className="text-emerald-400">Commit to main</strong>.</li>
                <li>Click <strong className="text-white">Publish Repository</strong> at the top bar to push it online!</li>
              </ol>
            </div>

            <div className="space-y-4">
              <h4 className="font-serif italic text-white flex items-center gap-2">
                <FileCode className="w-4 h-4 text-emerald-400" /> CLI Terminal Guide
              </h4>
              <p className="text-xs text-white/60 leading-relaxed font-sans">
                Prefer terminal command routines? Point your cmd terminal to your project root and execute:
              </p>

              <pre className="p-4 bg-black rounded-2xl text-[10px] text-emerald-400/85 font-mono overflow-x-auto border border-white/5">
{`# 1. Initialize local registry
git init

# 2. Stage files automatically
git add .

# 3. Create initial checkpoint
git commit -m "feat: first release"

# 4. Push directly online to GitHub
git branch -M main
git remote add origin YOUR_REPOSITORY_URL
git push -u origin main`}
              </pre>
            </div>

          </div>

          {/* Local Ollama Guide Panel */}
          <div className="p-6 rounded-2xl bg-[#111] border border-white/10 space-y-4 pt-6 mt-8">
            <h4 className="text-sm font-serif italic text-white flex items-center gap-2">
              <Terminal className="w-4 h-4 text-emerald-400" /> Air-Gapped Local Offline Protocol (Ollama)
            </h4>
            <p className="text-xs text-white/50 leading-relaxed font-sans">
              To host and process data strictly offline without sharing research PDF contents across public internet APIs:
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-[11px] leading-relaxed text-white/60">
              <div className="p-3 bg-white/[0.02] border border-white/5 rounded-xl">
                <span className="font-bold text-white block mb-1">1. Download Ollama</span>
                Install Ollama on your Windows/Mac/Linux system to serve models on local hardware with zero data leaks.
              </div>
              <div className="p-3 bg-white/[0.02] border border-white/5 rounded-xl">
                <span className="font-bold text-white block mb-1">2. Run Local Brain</span>
                Run <code className="text-emerald-400 bg-black px-1 py-0.5 rounded">ollama run mistral</code> or Llama3 models locally from your cmd.
              </div>
              <div className="p-3 bg-white/[0.02] border border-white/5 rounded-xl">
                <span className="font-bold text-white block mb-1">3. Point Server Endpoint</span>
                Point your raw Express <code className="text-emerald-400 bg-black px-1 py-0.5 rounded">/api/process-pdf</code> route to fetch your local ollama localhost URL!
              </div>
            </div>
          </div>

        </div>
      </div>

    </div>
  );
};

export default function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<StudyData | null>(null);
  const [filename, setFilename] = useState<string | null>(null);
  const [view, setView] = useState<'study' | 'quiz'>('study');
  const [activeTab, setActiveTab] = useState<'study' | 'dashboard'>('study');

  const handleUpload = async (file: File) => {
    setIsLoading(true);
    setError(null);
    setFilename(file.name);
    const formData = new FormData();
    formData.append('pdf', file);

    console.log("[Client] Uploading PDF:", file.name);

    try {
      const response = await fetch('/api/process-pdf', {
        method: 'POST',
        body: formData,
      });

      console.log("[Client] Server response received. Status:", response.status);

      if (!response.ok) {
        let errorMsg = "Upload failed";
        const contentType = response.headers.get("content-type");
        
        if (contentType && contentType.includes("application/json")) {
          const errData = await response.json();
          errorMsg = errData.error || errData.details || errorMsg;
        } else {
          try {
            const text = await response.text();
            console.error("[Client] Non-JSON response received:", text.substring(0, 100));
          } catch (_) {}
          
          if (response.status === 504) {
            errorMsg = "Gateway Timeout: The document processor timed out. Please try a smaller PDF file.";
          } else if (response.status === 503) {
            errorMsg = "Service Temporarily Busy: The processing queue is full. Please try again in 5-10 seconds.";
          } else if (response.status === 502) {
            errorMsg = "Bad Gateway: The cognitive server was restarted or busy. Please try again shortly.";
          } else {
            errorMsg = `System Error (${response.status}): The document pipeline is busy or returned an invalid format. Please try again.`;
          }
        }
        throw new Error(errorMsg);
      }

      const result = await response.json();
      console.log("[Client] Processing complete. Keycards:", result.keycards?.length);
      setData(result);
      setView('study');
    } catch (error) {
      console.error("[Client] Upload failed:", error);
      setError(error instanceof Error ? error.message : "Connection failed. Please verify that the development server is active.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col min-h-screen w-full bg-[#0a0a0a] text-[#e0e0e0] font-sans overflow-x-hidden selection:bg-emerald-500/30 selection:text-emerald-400">
      <Header filename={filename} activeTab={activeTab} onActiveTabChange={setActiveTab} />
      
      {activeTab === 'dashboard' ? (
        <main className="flex-1 p-8 md:p-12 overflow-y-auto max-h-[calc(100vh-64px)] scrollbar-hide animate-fadeIn">
          <div className="max-w-6xl mx-auto">
            <StudyDashboard 
              keycardCount={data?.keycards.length || 0}
              quizScore={data?.mcqs.length ? Math.round(data.mcqs.length * 0.8) : 0}
              totalMcqs={data?.mcqs.length || 0}
            />
          </div>
        </main>
      ) : (
        <main className="flex-1 flex flex-col md:flex-row overflow-hidden">
        {/* Left Sidebar - Design Aspect */}
        {data && (
           <aside className="w-full md:w-72 border-b md:border-b-0 md:border-r border-white/10 bg-[#0d0d0d] p-8 flex flex-col gap-10">
           <div className="space-y-6">
             <h2 className="text-[10px] uppercase tracking-[0.3em] text-white/20 font-bold">Source Control</h2>
             <button 
                onClick={() => { setData(null); setFilename(null); }}
                className="w-full p-6 border border-dashed border-white/10 rounded-2xl bg-white/5 flex flex-col items-center gap-4 text-center hover:border-emerald-500/40 hover:bg-white/[0.07] transition-all group"
             >
                <div className="w-12 h-12 rounded-full bg-emerald-500/10 flex items-center justify-center text-emerald-500 group-hover:scale-110 transition-transform">
                  <Upload className="w-5 h-5" />
                </div>
                <p className="text-[10px] uppercase tracking-widest font-bold text-white/50 group-hover:text-white transition-colors">Swap Source</p>
             </button>
           </div>
   
           <div className="space-y-6 flex-1">
             <h2 className="text-[10px] uppercase tracking-[0.3em] text-white/20 font-bold">Pipeline Status</h2>
             <div className="space-y-4">
               {[
                 { label: 'Extraction Active', done: true },
                 { label: `Keycards (${data.keycards.length})`, done: true },
                 { label: `Quiz Ready (${data.mcqs.length})`, done: true },
               ].map((step, i) => (
                 <div key={i} className="flex items-center gap-3">
                   <div className={cn(
                     "w-1.5 h-1.5 rounded-full transition-all duration-1000",
                     step.done ? "bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.8)]" : "bg-white/10"
                   )} />
                   <span className={cn("text-[10px] uppercase tracking-widest font-bold transition-colors", step.done ? "text-white/80" : "text-white/20")}>
                     {step.label}
                   </span>
                 </div>
               ))}
             </div>
           </div>
   
           <div className="p-6 rounded-2xl bg-gradient-to-br from-emerald-500/10 to-transparent border border-emerald-500/20">
             <p className="text-[10px] text-emerald-400 font-bold mb-2 uppercase tracking-[0.2em]">Voice Engine</p>
             <p className="text-[10px] uppercase tracking-widest text-white/60">Status: Active</p>
             <div className="mt-4 flex gap-1 h-3 items-end">
               {[0.8, 0.4, 0.6, 0.9, 0.7, 0.5, 0.8, 0.4].map((h, i) => (
                 <motion.div 
                   key={i}
                   animate={{ height: ['20%', '100%', '20%'] }}
                   transition={{ duration: 1.5, repeat: Infinity, delay: i * 0.1, ease: 'easeInOut' }}
                   className="w-1 bg-emerald-500 rounded-full"
                 />
               ))}
             </div>
           </div>
         </aside>
        )}

        {/* Content Area */}
        <div className="flex-1 p-8 md:p-12 overflow-y-auto max-h-[calc(100vh-64px)] scrollbar-hide">
          <div className="max-w-5xl mx-auto">
            {!data ? (
              <motion.div 
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="max-w-2xl mx-auto mt-20"
              >
                <FileUpload onUpload={handleUpload} isLoading={isLoading} error={error} />
              </motion.div>
            ) : (
              <div className="space-y-16 pb-20">
                <div className="flex flex-col sm:flex-row items-center justify-between gap-8 pb-10 border-b border-white/5">
                  <div className="flex items-center gap-6">
                    <div className="w-16 h-16 bg-white/5 border border-white/10 rounded-[1.5rem] flex items-center justify-center relative shadow-inner">
                      <FileText className="w-8 h-8 text-emerald-400 opacity-80" />
                      <div className="absolute -top-1 -right-1 w-4 h-4 bg-emerald-500 rounded-full border-4 border-[#0a0a0a]" />
                    </div>
                    <div>
                      <h3 className="text-2xl font-serif italic text-white/90">Cognitive Hub</h3>
                      <p className="text-[10px] text-white/30 font-mono font-bold tracking-widest uppercase mt-1">
                        High Fidelity Extraction Engine
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex bg-white/5 p-1 rounded-2xl border border-white/10 backdrop-blur-xl w-full sm:w-auto">
                    <button 
                      onClick={() => setView('study')}
                      className={cn(
                        "flex-1 sm:flex-none px-10 py-3 rounded-xl text-[10px] font-bold uppercase tracking-[0.2em] transition-all duration-300",
                        view === 'study' ? "bg-white text-black shadow-lg" : "text-white/40 hover:text-white/70"
                      )}
                    >
                      Insights
                    </button>
                    <button 
                      onClick={() => setView('quiz')}
                      className={cn(
                        "flex-1 sm:flex-none px-10 py-3 rounded-xl text-[10px] font-bold uppercase tracking-[0.2em] transition-all duration-300",
                        view === 'quiz' ? "bg-white text-black shadow-lg" : "text-white/40 hover:text-white/70"
                      )}
                    >
                      Quiz
                    </button>
                  </div>
                </div>

                <AnimatePresence mode="wait">
                  {view === 'study' ? (
                    <motion.div 
                      key="study"
                      initial={{ opacity: 0, y: 15 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -15 }}
                    >
                      <KeycardList cards={data.keycards} />
                    </motion.div>
                  ) : (
                    <motion.div 
                      key="quiz"
                      initial={{ opacity: 0, scale: 0.98 }}
                      animate={{ opacity: 1, scale: 1 }}
                      exit={{ opacity: 0, scale: 0.98 }}
                    >
                      <Quiz mcqs={data.mcqs} onRestart={() => { setData(null); setFilename(null); }} />
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            )}
          </div>
        </div>
      </main>
      )}

      <footer className="px-8 py-3 bg-[#080808] border-t border-white/5 flex flex-col sm:flex-row justify-between items-center gap-4">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 shadow-[0_0_5px_rgba(16,185,129,0.5)]"></div>
            <span className="text-[9px] uppercase tracking-[0.1em] text-white/40 font-bold">Secure PDF Pipeline</span>
          </div>
          <div className="h-3 w-px bg-white/5 hidden sm:block" />
          <span className="text-[9px] font-mono text-white/30 hidden sm:block uppercase">Extraction ver 1.5.24</span>
        </div>
        <p className="text-[9px] text-white/20 uppercase tracking-widest font-bold font-sans">
          &copy; 2026 Lumen Systems &middot; High Fidelity Reasoning Engine
        </p>
      </footer>
    </div>
  );
}
