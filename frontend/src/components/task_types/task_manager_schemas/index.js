import CategoricalTaskSchema from './CategoricalTaskSchema.json';
import OrdinalTaskSchema from './OrdinalTaskSchema.json';
import EntityTaskSchema from './EntityTaskSchema.json';
import AudioRegionTaskSchema from './AudioRegionTaskSchema.json';
import TextEditionTaskSchema from './TextEditionTaskSchema.json';
import TranscriptionTaskSchema from './TranscriptionTaskSchema.json';
import RealtimeVideoDimensionalTaskSchema from './RealtimeVideoDimensionalTaskSchema.json';
import EmotionCategoricalTaskSchema from './EmotionCategoricalTaskSchema.json';


const schema_files = import.meta.globEager('@/task_plugins/*/*Schema.json')

export default {
  CategoricalTaskSchema,
  OrdinalTaskSchema,
  EntityTaskSchema,
  AudioRegionTaskSchema,
  TextEditionTaskSchema,
  TranscriptionTaskSchema,
  RealtimeVideoDimensionalTaskSchema,
  EmotionCategoricalTaskSchema,
};
