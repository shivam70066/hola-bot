/*
  Warnings:

  - The primary key for the `hb_conversations` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `conversation_name` on the `hb_conversations` table. All the data in the column will be lost.
  - You are about to drop the column `id` on the `hb_conversations` table. All the data in the column will be lost.
  - Added the required column `conversation_title` to the `hb_conversations` table without a default value. This is not possible if the table is not empty.

*/
-- DropForeignKey
ALTER TABLE "hb_coversations_data" DROP CONSTRAINT "hb_coversations_data_conversation_id_fkey";

-- AlterTable
ALTER TABLE "hb_conversations" DROP CONSTRAINT "hb_conversations_pkey",
DROP COLUMN "conversation_name",
DROP COLUMN "id",
ADD COLUMN     "conversation_title" TEXT NOT NULL,
ALTER COLUMN "conversation_id" SET DATA TYPE TEXT,
ADD CONSTRAINT "hb_conversations_pkey" PRIMARY KEY ("conversation_id");

-- AlterTable
ALTER TABLE "hb_coversations_data" ALTER COLUMN "conversation_id" SET DATA TYPE TEXT;

-- AddForeignKey
ALTER TABLE "hb_coversations_data" ADD CONSTRAINT "hb_coversations_data_conversation_id_fkey" FOREIGN KEY ("conversation_id") REFERENCES "hb_conversations"("conversation_id") ON DELETE RESTRICT ON UPDATE CASCADE;
