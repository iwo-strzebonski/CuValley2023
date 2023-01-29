// HACK: Only because VSC incorrectly marks the Object.values() function as not existing
export declare global {
  interface Object {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    values: (object: { [key: string]: any }) => any[]
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    fromEntries: (entries: [string, any][]) => { [key: string]: any }
  }
}
