import { z } from "zod";

export const pitchDeckSchema = z.object({
  file: z
    .custom<FileList>((val) => val instanceof FileList, "Please select a file")
    .refine((files) => files.length > 0, "File is required")
    .refine((files) => files[0].type === "application/pdf", "Only PDF files are supported")
    .refine((files) => files[0].size <= 10 * 1024 * 1024, "File size must be less than 10MB"),
  startup_id: z.string().min(1, "Startup ID is required"),
});

export type PitchDeckFormData = z.infer<typeof pitchDeckSchema>;

export const startupSchema = z.object({
  startup_name: z.string().min(2, "Name must be at least 2 characters"),
  industry: z.string().min(1, "Please select an industry"),
  stage: z.string().min(1, "Please select a stage"),
  funding_needed: z.number().min(0, "Funding must be a positive number"),
});

export type StartupFormData = z.infer<typeof startupSchema>;
