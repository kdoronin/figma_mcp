// Progress tracking service

import { ProgressUpdate } from '../types';
import { PROGRESS_STATUS } from '../constants';

export class ProgressService {
  static createProgressUpdate(
    commandId: string,
    commandType: string,
    status: keyof typeof PROGRESS_STATUS,
    progress: number,
    totalItems: number,
    processedItems: number,
    message: string,
    payload: any = null
  ): ProgressUpdate {
    const update: ProgressUpdate = {
      type: "command_progress",
      commandId,
      commandType,
      status: PROGRESS_STATUS[status] as ProgressUpdate['status'],
      progress,
      totalItems,
      processedItems,
      message,
      timestamp: Date.now(),
    };

    // Add optional chunk information if present
    if (payload) {
      if (
        payload.currentChunk !== undefined &&
        payload.totalChunks !== undefined
      ) {
        update.currentChunk = payload.currentChunk;
        update.totalChunks = payload.totalChunks;
        update.chunkSize = payload.chunkSize;
      }
      update.payload = payload;
    }

    return update;
  }

  static sendProgressUpdate(
    commandId: string,
    commandType: string,
    status: keyof typeof PROGRESS_STATUS,
    progress: number,
    totalItems: number,
    processedItems: number,
    message: string,
    payload: any = null
  ): ProgressUpdate {
    const update = this.createProgressUpdate(
      commandId,
      commandType,
      status,
      progress,
      totalItems,
      processedItems,
      message,
      payload
    );

    // Send to UI - this will be handled by the caller
    console.log(`Progress update: ${status} - ${progress}% - ${message}`);

    return update;
  }
}